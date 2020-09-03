
import asyncio

from tornado.web import authenticated, HTTPError
from async_generator import aclosing

from jupyterhub.apihandlers.users import SpawnProgressAPIHandler
from jupyterhub.utils import iterate_until

from ..orm import Dashboard
from ..util import url_path_join
from ..app import BuildersStore


class ProgressDashboardHandler(SpawnProgressAPIHandler):

    @authenticated
    async def get(self, dashboard_urlname=''):
        self.set_header('Cache-Control', 'no-cache')

        current_user = await self.get_current_user()

        dashboard = self.db.query(Dashboard).filter(Dashboard.urlname==dashboard_urlname).one_or_none()

        if dashboard is None:
            raise HTTPError(404, 'No such dashboard or user')

        if not dashboard.is_orm_user_allowed(current_user.orm_user):
            raise HTTPError(403, 'User {} not authorized to access dashboard {}'.format(current_user.name, dashboard.urlname))
        

        # start sending keepalive to avoid proxies closing the connection
        asyncio.ensure_future(self.keepalive())
        # cases:
        # - spawner already started and ready
        # - spawner not running at all
        # - spawner failed
        # - spawner pending start (what we expect)
        def ready_event(dashboard):
            url = url_path_join(self.settings['base_url'], "user", dashboard.user.name, dashboard.final_spawner.name)
            return {
                'progress': 100,
                'ready': True,
                'message': "Redirecting to server at {}".format(url),
                'html_message': 'Redirecting to server at <a href="{0}" target="_blank">{0}</a>'.format(url),
                'url': url,
            }

        failed_event = {'progress': 100, 'failed': True, 'message': "Build failed or unable to get progress", 
            'url': url_path_join(self.settings['base_url'], "hub", "dashboards", dashboard.urlname, 'clear-error')
            }


        builders_store = BuildersStore.get_instance(self.settings['config'])

        builder = builders_store[dashboard]

        if builder.ready:
            # spawner already ready. Trigger progress-completion immediately
            self.log.info("Server %s is already started", builder._log_name)
            await self.send_event(ready_event(dashboard))
            return

        build_future = builder._build_future

        if not builder._build_pending:
            # not pending, no progress to fetch
            # check if spawner has just failed
            f = build_future
            if f and f.done() and f.exception():
                failed_event['message'] = "Build failed: %s" % f.exception()
                await self.send_event(failed_event)
                return
            else:
                raise HTTPError(400, "%s is not starting...", builder._log_name)

        if build_future: # Just in case build_future is None so iterate_until's asyncio.wait doesn't fail; 
            # builder._generate_progress should return an iterator because _build_pending was non-None
            # just above, with no awaits since

            # Retrieve progress events from the Builder
            async with aclosing(
                iterate_until(build_future, builder._generate_progress())
            ) as events:
                try:
                    async for event in events:
                        # don't allow events to sneakily set the 'ready' flag
                        if 'ready' in event:
                            event.pop('ready', None)
                        await self.send_event(event)
                except asyncio.CancelledError:
                    pass

            # progress finished, wait for spawn to actually resolve,
            # in case progress finished early
            # (ignore errors, which will be logged elsewhere)
            await build_future

        # progress and spawn finished, check if spawn succeeded
        if builder.ready:
            # spawner is ready, signal completion and redirect
            self.log.info("Server %s is ready", builder._log_name)
            await self.send_event(ready_event(dashboard))
        else:
            # what happened? Maybe spawn failed?
            f = build_future
            if f and f.done() and f.exception():
                failed_event['message'] = "Build failed: %s" % f.exception()
            else:
                self.log.warning(
                    "Server %s didn't start for unknown reason", builder._log_name
                )
            await self.send_event(failed_event)




import re
from datetime import datetime
from collections import defaultdict
from asyncio import sleep, CancelledError

from async_generator import aclosing
from tornado.web import HTTPError
from tornado.log import app_log

from jupyterhub.orm import User
from jupyterhub.utils import iterate_until

from ..util import maybe_future
from ..orm import Dashboard
from ..app import BuildersStore
from ..dbutil import is_upgrade_needed

def check_database_upgrade(f):
    def handler(self, *args, **kwargs):
        engine = self.db.get_bind()
        if is_upgrade_needed(engine):
            return self.redirect("{}hub/dashboards-db-upgrade".format(self.settings['base_url']))
        return f(self, *args, **kwargs)
    return handler


class DashboardBaseMixin:

    unsafe_regex = re.compile(r'[^a-zA-Z0-9]+')

    trailingdash_regex = re.compile(r'\-+$')

    name_regex = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9_\- \!\@\$\(\)\*\+\?\<\>\.]{0,99}$')

    start_path_regex = re.compile(r'^[A-Za-z0-9\-\._~\:\/\?#\[\]@\!\$\&\(\)\*\+ ,;\%\=]*$')

    def calc_urlname(self, dashboard_name):
        base_urlname = re.sub(self.unsafe_regex, '-', dashboard_name).lower()[:35]

        base_urlname = re.sub(self.trailingdash_regex, '', base_urlname)

        urlname = base_urlname

        self.log.debug('calc safe name from '+urlname)

        now_unique = False
        counter = 1
        while not now_unique:
            orm_dashboard = Dashboard.find(db=self.db, urlname=urlname)
            self.log.info("{} - {}".format(urlname, orm_dashboard))
            if orm_dashboard is None or counter >= 100:
                now_unique = True
            else:
                urlname = "{}-{}".format(base_urlname, counter)
                counter += 1

        self.log.debug('calc safe name : '+urlname)
        return urlname

    @staticmethod
    async def pipe_spawner_progress(dashboard_user, new_server_name, builder):
        
        while True:

            await sleep(0.01)

            if builder._build_future.done():
                break

            if new_server_name in dashboard_user.spawners and dashboard_user.spawners[new_server_name].pending \
                and dashboard_user.spawners[new_server_name]._spawn_future:

                spawner = dashboard_user.spawners[new_server_name]

                app_log.debug('Found spawner for progress')

                async with aclosing(
                    iterate_until(builder._build_future, spawner._generate_progress())
                ) as spawnevents:
                    try:
                        async for event in spawnevents:
                            if 'message' in event:
                                builder.add_progress_event({
                                    'progress': 95, 'message': 'Spawner progress: {}'.format(event['message'])
                                    })
                    except CancelledError:
                        pass

                break 

    def get_source_spawners(self, user):
        return [spawner for spawner in user.all_spawners(include_default=True) if not spawner.orm_spawner.dashboard_final_of]

    def get_visitor_dashboards(self, user):
        orm_dashboards = set()

        for group in user.groups:
            if group.dashboard_visitors_for:
                orm_dashboards.add(group.dashboard_visitors_for)

        orm_dashboards.update(self.db.query(Dashboard).filter(Dashboard.allow_all==True).filter(Dashboard.user != user.orm_user).all())

        user_dashboard_groups = defaultdict(list)

        for dash in orm_dashboards:
            if dash.user: # Just in case it's null due to db corruption
                user_dashboard_groups[dash.user.name].append(dash)

        return user_dashboard_groups

    def get_visitor_users(self, exclude_user_id):
        return self.db.query(User).filter(User.id != exclude_user_id).all()

    def get_visitor_tuples(self, exclude_user_id, existing_group_users=None):
        possible_visitor_users = self.get_visitor_users(exclude_user_id)

        visitor_users = []

        if existing_group_users is not None:
            visitor_users = existing_group_users

        return [(True, user) for user in visitor_users] + [(False, user) for user in set(possible_visitor_users) - set(visitor_users)]

    async def maybe_start_build(self, dashboard, dashboard_user, force_start=False):

        builders_store = BuildersStore.get_instance(self.settings['config'])

        builder = builders_store[dashboard]

        need_follow_progress = True

        def do_final_build(f):
            if f.cancelled() or f.exception() is None:
                builder._build_future = None
            builder._build_pending = False

        if not builder.pending and (dashboard.final_spawner is None or force_start):
            
            if builder._build_future and builder._build_future.done() and builder._build_future.exception() and not force_start:
                pass # Progress stream should display the error for us

            else:
                self.log.debug('starting builder')

                builder._build_pending = True

                async def do_build():

                    # This section would be better if it was inside dockerbuilder, but we want 
                    # to make use of self.spawn_single_user without repeating the code
                    if dashboard.source_spawner and dashboard.source_spawner.name:

                        # Get source spawner
                        source_spawner = dashboard_user.spawners[dashboard.source_spawner.name]

                        if source_spawner.ready:
                            self.log.debug('Source spawner is already ready')
                        elif source_spawner.pending in ['spawn', 'check']:
                            builder.add_progress_event({'progress': 15, 'message': 'Attacheding to pending source server for Dashboard'})
                            self.log.debug('Source spawner is pending - await')
                            spawn_future = final_spawner.getattr('_{}_future'.format(final_spawner.pending), None)
                            if spawn_future:
                                await spawn_future
                        else:
                            builder.add_progress_event({'progress': 10, 'message': 'Starting up source server for Dashboard'})
                            self.log.debug('Source spawner needs a full start')
                            await self.spawn_single_user(dashboard_user, dashboard.source_spawner.name)

                    # Delete existing final spawner if it exists
                    await self.maybe_delete_existing_server(dashboard.final_spawner, dashboard_user)

                    (new_server_name, new_server_options) =  await builder.start(dashboard, dashboard_user, self.db)

                    builder.add_progress_event({'progress': 80, 'message': 'Starting up final server for Dashboard, after build'})

                    maybe_future(self.pipe_spawner_progress(dashboard_user, new_server_name, builder))

                    await self.spawn_single_user(dashboard_user, new_server_name, options=new_server_options)

                    self.db.expire(dashboard) # May have changed during async code above

                    if new_server_name in dashboard_user.orm_user.orm_spawners:
                        dashboard.final_spawner = dashboard_user.orm_user.orm_spawners[new_server_name]

                    # TODO if not, then what?

                    dashboard.started = datetime.utcnow()

                    self.db.commit()

                builder._build_future = maybe_future(do_build())

                builder._build_future.add_done_callback(do_final_build)

        elif builder.pending:
            pass # Progress will show where we've got to

        elif dashboard.final_spawner:
            user = self._user_from_orm(dashboard_user)

            final_spawner = user.spawners[dashboard.final_spawner.name]

            if final_spawner.ready:
                need_follow_progress = False

            elif final_spawner.pending:

                if final_spawner.pending in ['spawn', 'check']:
                    builder._build_pending = True

                    builder.add_progress_event({'progress': 90, 'message': 'Attaching to spawn of final server for Dashboard'})

                    # TODO This branch is rare, but should attach pipe to spawner progress

                    final_spawner.getattr('_{}_future'.format(final_spawner.pending)).add_done_callback(do_final_build)

                else:
                    builder.add_progress_event({'failed': True, 'message': 'Final server for Dashboard is Stopping'})

            else:

                builder._build_pending = True

                builder.event_queue = []

                builder.add_progress_event({'progress': 80, 'message': 'Starting up final server for Dashboard'})

                maybe_future(self.pipe_spawner_progress(user, final_spawner.name, builder))

                builder._build_future = maybe_future(self.spawn_single_user(user, final_spawner.name))

                builder._build_future.add_done_callback(do_final_build)

        return need_follow_progress

    async def maybe_delete_existing_server(self, orm_spawner, dashboard_user):
        if not orm_spawner:
            return
        
        server_name = orm_spawner.name

        user = self._user_from_orm(dashboard_user)

        spawner = user.spawners[server_name]

        if server_name:
            if not self.allow_named_servers:
                raise HTTPError(400, "Named servers are not enabled.")
            if server_name not in user.orm_spawners:
                self.log.debug("%s does not exist anyway", spawner._log_name)
                return
        else:
            raise HTTPError(400, "Cannot delete the default server")

        if spawner.pending == 'stop':
            self.log.debug("%s already stopping", spawner._log_name)

            await spawner._stop_future

        if spawner.ready or spawner.pending == 'spawn':

            if spawner.pending == 'spawn':
                self.log.debug("%s awaiting spawn to finish so can shut it down", spawner._log_name)
                await spawner._spawn_future

            # include notify, so that a server that died is noticed immediately
            status = await spawner.poll_and_notify()
            if status is None:
                stop_future = await self.stop_single_user(user, server_name)
                await stop_future

        self.log.info("Deleting spawner %s", spawner._log_name)
        self.db.delete(spawner.orm_spawner)
        user.spawners.pop(server_name, None)
        self.db.commit()


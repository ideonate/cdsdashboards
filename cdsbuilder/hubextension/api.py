from tornado.web import authenticated, HTTPError

from jupyterhub.apihandlers.base import APIHandler

from ..orm import Dashboard
from .base import DashboardBaseMixin


class DashboardBaseAPIHandler(APIHandler, DashboardBaseMixin):
    pass


class DashboardAPIHandler(DashboardBaseAPIHandler):

    @authenticated
    async def delete(self, user_name, dashboard_urlname):

        current_user = await self.get_current_user()

        if current_user.name != user_name:
            raise HTTPError(400, "Dashboard does not belong to current user.")

        dashboard = self.db.query(Dashboard).filter(Dashboard.urlname==dashboard_urlname).one_or_none()

        if dashboard is None:
            raise HTTPError(404, "Dashboard does not exist.")

        if dashboard.user.name != current_user.name: # Shouldn't really happen, trapped above unless db corrupt
            raise HTTPError(400, 'Dashboard user {} does not match {}'.format(dashboard.user.name, current_user.name))

        # options = self.get_json_body()

        builders_store = self.settings['cds_builders']

        builder = builders_store[dashboard]

        if builder.pending:
            raise HTTPError(400, 'Dashboard {} is currently building. Please try again once complete.'.format(dashboard_urlname))

        try:
        
            await self.maybe_delete_existing_server(dashboard.final_spawner, current_user)

            # TODO check delete went OK

            self.log.info("Deleting dashboard %s", dashboard_urlname)

            self.db.expire(dashboard)

            if dashboard in builders_store:
                del builders_store[dashboard]

            self.db.delete(dashboard)

            self.db.commit()

        except Exception as e:
            raise HTTPError(500, 'Error removing dashboard {}: {}'.format(dashboard_urlname, e))

        self.set_header('Content-Type', 'text/plain')
        self.set_status(202)

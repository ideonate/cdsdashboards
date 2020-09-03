import json

from tornado.web import authenticated, HTTPError

from jupyterhub.apihandlers.base import APIHandler
from jupyterhub.utils import url_path_join

from ..orm import Dashboard
from .base import DashboardBaseMixin
from ..app import BuildersStore


class DashboardBaseAPIHandler(APIHandler, DashboardBaseMixin):
    
    def check_referer(self):  # These request is allowed from user server
        """Check Origin for cross-site API requests.

        Copied from WebSocket with changes:

        - allow unspecified host/referer (e.g. scripts)
        """
        host = self.request.headers.get("Host")
        referer = self.request.headers.get("Referer")

        # If no header is provided, assume it comes from a script/curl.
        # We are only concerned with cross-site browser stuff here.
        if not host:
            self.log.warning("Blocking API request with no host")
            return False
        if not referer:
            self.log.warning("Blocking API request with no referer")
            return False

        host_path = url_path_join(host, self.hub.base_url)
        user_path = url_path_join(host, 'user/')
        referer_path = referer.split('://', 1)[-1] + '/'
        if not referer_path.startswith(host_path) and not referer_path.startswith(user_path):
            self.log.warning(
                "Blocking Cross Origin API request.  Referer: %s, Host: %s, User host: %s",
                referer,
                host_path,
                user_path
            )
            return False

        return True


class DashboardsAPIHandler(DashboardBaseAPIHandler):

    @authenticated
    async def get(self):
        """Return the list of dashboards for the current user."""

        current_user = await self.get_current_user()

        def to_json(dashboard):
            return {
                "name": dashboard.name,
                "url": "{}hub/dashboards/{}".format(self.settings['base_url'], dashboard.urlname),
                "description": dashboard.description,
                "path": dashboard.start_path,
                "username": dashboard.user.name
            }

        my_dashboards = current_user.dashboards_own
        body = {"_owned": list(map(to_json, my_dashboards))}

        visitor_dashboard_groups = self.get_visitor_dashboards(current_user)
        for username, dashboards in visitor_dashboard_groups.items():
            body[username] = list(map(to_json, dashboards))

        self.set_status(200)
        self.finish(json.dumps(body))


class DashboardDeleteAPIHandler(DashboardBaseAPIHandler):

    @authenticated
    async def delete(self, dashboard_urlname):

        current_user = await self.get_current_user()

        dashboard = self.db.query(Dashboard).filter(Dashboard.urlname==dashboard_urlname).one_or_none()

        if dashboard is None:
            raise HTTPError(404, "Dashboard does not exist.")

        if dashboard.user.name != current_user.name:
            raise HTTPError(403, 'This is not your dashboard: dashboard user {} does not match you ({})'.format(dashboard.user.name, current_user.name))

        # options = self.get_json_body()

        builders_store = BuildersStore.get_instance(self.settings['config'])

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


class UserSelfAPIHandler(DashboardBaseAPIHandler):

    @authenticated
    async def get(self):
        """Return the current user."""

        current_user = await self.get_current_user()

        self.set_status(200)
        self.finish(json.dumps(self.user_model(current_user)))

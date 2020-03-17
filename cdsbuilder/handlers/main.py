from tornado.web import authenticated, gen

from .base import BaseHandler


class MainDashboardHandler(BaseHandler):

    @authenticated
    async def get(self, user_name, server_name=''):

        dashboard_store = self.settings['dashboard']

        self.log.debug('calling get_app_server')

        dashboard = await dashboard_store.get_app_server(user_name, server_name)

        self.render_template(
            "appconfig.html",
            base_url=self.settings['base_url'],
            user_name=user_name,
            server_name=server_name,
            dashboard=dashboard,
            extra_footer_scripts=self.settings['extra_footer_scripts'],
        )

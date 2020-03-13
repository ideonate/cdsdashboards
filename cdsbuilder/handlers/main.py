from tornado.web import authenticated

from .base import BaseHandler


class MainHandler(BaseHandler):

    @authenticated
    def get(self, user_name, server_name=''):
        self.render_template(
            "appconfig.html",
            base_url=self.settings['base_url'],
            user_name=user_name,
            server_name=server_name,
            extra_footer_scripts=self.settings['extra_footer_scripts'],
        )

from tornado import web
from tornado.log import app_log
#from jupyterhub.services.auth import HubOAuthenticated, HubOAuth


class BaseHandler(web.RequestHandler): # HubOAuthenticated
    """HubAuthenticated by default allows all successfully identified users (see allow_all property)."""

    def initialize(self):
        super().initialize()
        self.log = app_log
        #self.hub_auth = HubOAuth.instance(config=self.settings['traitlets_config'])

    @property
    def template_namespace(self):
        return dict(static_url=self.static_url,
                    **self.settings.get('template_variables', {}))

    def render_template(self, name, **extra_ns):
        """Render an HTML page"""
        ns = {}
        ns.update(self.template_namespace)
        ns.update(extra_ns)
        template = self.settings['jinja2_env'].get_template(name)
        html = template.render(**ns)
        self.write(html)

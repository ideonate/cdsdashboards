import os

from traitlets import Bool
from traitlets.config import SingletonConfigurable

from jupyterhub.handlers.static import CacheControlStaticFilesHandler

from .main import AllDashboardsHandler, DashboardEditHandler, MainViewDashboardHandler, ClearErrorDashboardHandler
from .events import ProgressDashboardHandler
from .._data import DATA_FILES_PATH
from .api import DashboardAPIHandler


cds_extra_handlers = [
    
    (r'dashboards-new', DashboardEditHandler),

    (r'dashboards', AllDashboardsHandler),
    
    (r'dashboards/(?P<dashboard_urlname>[^/]+?)/edit', DashboardEditHandler, {}, 'cds_dashboard_config_handler'),
    (r'dashboards/(?P<dashboard_urlname>[^/]+?)', MainViewDashboardHandler),
    (r'dashboards/(?P<dashboard_urlname>[^/]+?)/clear-error', ClearErrorDashboardHandler),

    (r'dashboards-static/(.*)', CacheControlStaticFilesHandler, dict(path=os.path.join(DATA_FILES_PATH, 'static'))),

    (r'dashboards-api/(?P<dashboard_urlname>[^/]+?)', DashboardAPIHandler),
    (r'dashboards-api/(?P<dashboard_urlname>[^/]+?)/progress', ProgressDashboardHandler),
]

class CDSConfig(SingletonConfigurable):

    # Settings really for JupyterHub entry point

    jh_show_user_named_servers = Bool(
        True,
        help="""
        Show the user their regular named servers table on home page.
        Since c.JupyterHub.allow_named_servers should be set to True, so admins can control all servers if needed, 
        you can use this flag to hide the named servers section from users.
        """,
        config=True
    )

    jh_show_user_dashboard_servers = Bool(
        True,
        help="""
        Show the user their dashboard servers table on home page.
        Since c.JupyterHub.allow_named_servers should be set to True, so admins can control all servers if needed, 
        you can use this flag to hide the dashboard servers section from users.
        """,
        config=True
    )

    _dc = None

    @classmethod
    def set_config(cls, c):
        cls._dc = c

    @classmethod
    def get_template_vars(cls):
        conf = cls.instance(config=cls._dc)
        return {
            'cds_jh_show_user_named_servers' : conf.jh_show_user_named_servers,
            'cds_jh_show_user_dashboard_servers' : conf.jh_show_user_dashboard_servers
            }

__all__ = ['CDSConfig', 'cds_extra_handlers']

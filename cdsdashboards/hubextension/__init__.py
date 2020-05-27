import os

from traitlets import Bool
from traitlets.config import SingletonConfigurable

from jupyterhub.handlers.static import CacheControlStaticFilesHandler

from .main import AllDashboardsHandler, DashboardEditHandler, MainViewDashboardHandler, ClearErrorDashboardHandler, UpgradeDashboardsHandler
from .events import ProgressDashboardHandler
from .._data import DATA_FILES_PATH
from .api import DashboardAPIHandler


cds_extra_handlers = [
    
    (r'dashboards-db-upgrade', UpgradeDashboardsHandler),

    (r'dashboards-new', DashboardEditHandler),

    (r'dashboards', AllDashboardsHandler),
    
    (r'dashboards/(?P<dashboard_urlname>[^/]+?)/edit', DashboardEditHandler, {}, 'cds_dashboard_config_handler'),
    (r'dashboards/(?P<dashboard_urlname>[^/]+?)', MainViewDashboardHandler),
    (r'dashboards/(?P<dashboard_urlname>[^/]+?)/clear-error', ClearErrorDashboardHandler),

    (r'dashboards-static/(.*)', CacheControlStaticFilesHandler, dict(path=os.path.join(DATA_FILES_PATH, 'static'))),

    (r'dashboards-api/(?P<dashboard_urlname>[^/]+?)', DashboardAPIHandler),
    (r'dashboards-api/(?P<dashboard_urlname>[^/]+?)/progress', ProgressDashboardHandler),

]

def config_for_dashboards(c):
    """
    Add the required configuration to the Configurable object to enable Dashboards
    TODO extend any settings that are already present in c
    """

    from ..app import CDS_TEMPLATE_PATHS, cds_tornado_settings

    c.JupyterHub.extra_handlers = cds_extra_handlers
    c.JupyterHub.tornado_settings = cds_tornado_settings
    c.JupyterHub.template_paths = CDS_TEMPLATE_PATHS

    return c

__all__ = ['cds_extra_handlers', 'config_for_dashboards']

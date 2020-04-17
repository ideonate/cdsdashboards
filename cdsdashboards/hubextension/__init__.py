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

__all__ = ['cds_extra_handlers']

import os
from jupyterhub.handlers.static import CacheControlStaticFilesHandler
from .main import AllDashboardsHandler, DashboardNewHandler, DashboardEditHandler, MainViewDashboardHandler, ClearErrorDashboardHandler
from .events import ProgressDashboardHandler
from .._data import DATA_FILES_PATH


extra_handlers = [
    (r'dashboards', AllDashboardsHandler),
    (r'dashboards/new', DashboardNewHandler),
    (r'dashboards-static/(.*)', CacheControlStaticFilesHandler, dict(path=os.path.join(DATA_FILES_PATH, 'static'))),
    (r'dashboards/(?P<user_name>[^/]+)/(?P<dashboard_urlname>[^/]+?)/edit', DashboardEditHandler, {}, 'cds_dashboard_config_handler'),
    (r'dashboards/(?P<user_name>[^/]+)/(?P<dashboard_urlname>[^/]+?)', MainViewDashboardHandler),
    (r'dashboards/(?P<user_name>[^/]+)/(?P<dashboard_urlname>[^/]+?)/clear-error', ClearErrorDashboardHandler),
    (r'dashboards/(?P<user_name>[^/]+)/(?P<dashboard_urlname>[^/]+?)/progress', ProgressDashboardHandler),
]

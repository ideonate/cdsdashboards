from .main import MainDashboardHandler

extra_handlers = [
    (r'dashboards/(?P<user_name>[^/]+)/app/(?P<server_name>[^/]+?)', MainDashboardHandler)
]

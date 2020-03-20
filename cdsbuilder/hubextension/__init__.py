from .main import AllDashboardsHandler, DashboardNewHandler, DashboardEditHandler

extra_handlers = [
    (r'dashboards', AllDashboardsHandler),
    (r'dashboards/new', DashboardNewHandler),
    (r'dashboards/(?P<user_name>[^/]+)/(?P<dashboard_urlname>[^/]+?)/edit', DashboardEditHandler, {}, 'cds_dashboard_config_handler'),
    
    #(r'dashboards/(?P<user_name>[^/]+)/(?P<dashboard_name>[^/]+?)', MainViewDashboardHandler)
]

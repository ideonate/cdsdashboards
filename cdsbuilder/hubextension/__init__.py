from .main import AllDashboardsHandler, DashboardNewHandler, DashboardConfigHandler

extra_handlers = [
    (r'dashboards/', AllDashboardsHandler),
    (r'dashboards/new', DashboardNewHandler),
    (r'dashboards/(?P<user_name>[^/]+)/(?P<dashboard_name>[^/]+?)/edit', DashboardConfigHandler, {}, 'cds_dashboard_config_handler'),
    
    #(r'dashboards/(?P<user_name>[^/]+)/(?P<dashboard_name>[^/]+?)', MainViewDashboardHandler)
]

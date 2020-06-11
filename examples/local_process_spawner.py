c.JupyterHub.db_url = 'sqlite:///examples/sqlitedbs/local_process_spawner.sqlite'

c.JupyterHub.authenticator_class = 'jupyterhub.auth.DummyAuthenticator'

c.JupyterHub.spawner_class = 'cdsdashboards.hubextension.spawners.VariableLocalProcessSpawner'

c.CDSDashboardsConfig.builder_class = 'cdsdashboards.builder.processbuilder.ProcessBuilder'

c.LocalProcessSpawner.debug = True

c.LocalProcessSpawner.notebook_dir = '/Users/dan/Dev/cdsdashboards/examples/local_process_folder/{username}'

c.Spawner.start_timeout = 6000

c.Spawner.debug = True

c.Authenticator.admin_users = {'dan'}

c.ConfigurableHTTPProxy.debug = True

c.JupyterHub.allow_named_servers = True

#c.VariableLocalProcessSpawner.proxy_request_timeout = 300


from cdsdashboards.app import CDS_TEMPLATE_PATHS
from cdsdashboards.hubextension import cds_extra_handlers

c.JupyterHub.template_paths = CDS_TEMPLATE_PATHS
c.JupyterHub.extra_handlers = cds_extra_handlers


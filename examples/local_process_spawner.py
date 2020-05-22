
c.JupyterHub.authenticator_class = 'jupyterhub.auth.DummyAuthenticator'

c.JupyterHub.spawner_class = 'cdsdashboards.hubextension.spawners.VariableLocalProcessSpawner'

c.LocalProcessSpawner.debug = True

c.LocalProcessSpawner.notebook_dir = '/Users/dan/Dev/cdsdashboards/examples/local_process_folder'

c.Spawner.start_timeout = 6000

c.Authenticator.admin_users = {'dan'}

c.ConfigurableHTTPProxy.debug = True

c.JupyterHub.allow_named_servers = True



from cdsdashboards.app import CDS_TEMPLATE_PATHS, cds_tornado_settings
from cdsdashboards.hubextension import cds_extra_handlers

c.JupyterHub.template_paths = CDS_TEMPLATE_PATHS
c.JupyterHub.tornado_settings = cds_tornado_settings
c.JupyterHub.extra_handlers = cds_extra_handlers

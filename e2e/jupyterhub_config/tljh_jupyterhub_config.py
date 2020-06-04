
c.JupyterHub.authenticator_class = 'jupyterhub.auth.DummyAuthenticator'

c.JupyterHub.spawner_class = 'cdsdashboards.hubextension.spawners.variableusercreating.VariableUserCreatingSpawner'

c.CDSDashboardsConfig.builder_class = 'cdsdashboards.builder.processbuilder.ProcessBuilder'

c.SystemdSpawner.unit_name_template = 'jupyter-{USERNAME}{DASHSERVERNAME}'

c.Spawner.notebook_dir = '/home/jupyter-{username}'

c.Authenticator.admin_users = {'dan'}

c.JupyterHub.allow_named_servers = True

from cdsdashboards.app import CDS_TEMPLATE_PATHS
from cdsdashboards.hubextension import cds_extra_handlers

c.JupyterHub.template_paths = CDS_TEMPLATE_PATHS
c.JupyterHub.extra_handlers = cds_extra_handlers

c.Spawner.debug = True

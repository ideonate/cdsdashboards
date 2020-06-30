import os

c.JupyterHub.bind_url = 'https://0.0.0.0:80'

c.JupyterHub.authenticator_class = 'jupyterhub.auth.DummyAuthenticator'

c.Authenticator.admin_users = {'dan'}
c.Authenticator.whitelist = {'dan'}


c.JupyterHub.allow_named_servers = True

from cdsdashboards.app import CDS_TEMPLATE_PATHS
from cdsdashboards.hubextension import cds_extra_handlers

c.JupyterHub.template_paths = CDS_TEMPLATE_PATHS
c.JupyterHub.extra_handlers = cds_extra_handlers

c.Spawner.debug = True

from dockerspawner import DockerSpawner

from jupyter_client.localinterfaces import public_ips

c.JupyterHub.hub_ip = public_ips()[0]


c.JupyterHub.spawner_class = DockerSpawner

c.CDSDashboardsConfig.builder_class = 'cdsdashboards.builder.dockerbuilder.DockerBuilder'

#from jupyter_client.localinterfaces import public_ips

#c.JupyterHub.hub_ip = public_ips()[0]

c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = 'e2etestnetwork'
# Pass the network name as argument to spawned containers
c.DockerSpawner.extra_host_config = { 'network_mode': 'e2etestnetwork' }


notebook_dir = '/home/jovyan'
c.DockerSpawner.notebook_dir = notebook_dir

JH_CYPRESS_DOCKER_EXTERNAL_USERHOME = os.environ['JH_CYPRESS_DOCKER_EXTERNAL_USERHOME']

c.DockerSpawner.volumes = {
    "{}/{}".format(JH_CYPRESS_DOCKER_EXTERNAL_USERHOME, '{username}'): notebook_dir
}

c.DockerSpawner.remove = True

c.DockerSpawner.name_template = "tests-{prefix}-{username}-{servername}"

c.DockerSpawner.image = 'ideonate/containds-all-basic:0.0.20'


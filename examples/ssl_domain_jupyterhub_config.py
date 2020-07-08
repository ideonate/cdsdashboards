
c.JupyterHub.allow_named_servers = True


from cdsdashboards.hubextension import config_for_dashboards

config_for_dashboards(c)


c.JupyterHub.template_vars = {'cds_hide_user_named_servers': False, 'cds_hide_user_dashboard_servers': False}


c.JupyterHub.authenticator_class = 'jupyterhub.auth.DummyAuthenticator'

c.JupyterHub.bind_url = 'https://0.0.0.0:443'

c.JupyterHub.db_url = 'sqlite:///examples/sqlitedbs/ssl_domain_jupyterhub_config.sqlite'

c.JupyterHub.default_url = '/hub/home'

c.JupyterHub.proxy_check_interval = 3000

c.JupyterHub.service_check_interval = 6000

# To try idle culling
# export JUPYTERHUB_API_TOKEN=$(jupyterhub token)
# python3 -m jupyterhub_idle_culler --timeout=10 --url=http://192.168.0.69:8081/hub/api
c.JupyterHub.last_activity_interval = 30

c.JupyterHub.spawner_class = 'cdsdashboards.hubextension.spawners.variabledocker.VariableDockerSpawner'

c.CDSDashboardsConfig.builder_class = 'cdsdashboards.builder.dockerbuilder.DockerBuilder'

from jupyter_client.localinterfaces import public_ips

c.JupyterHub.hub_ip = public_ips()[0]

c.DockerSpawner.debug = True

#c.DockerSpawner.go_slow = True


c.CDSDashboardsConfig.show_source_servers = False
c.CDSDashboardsConfig.require_source_server = False

c.CDSDashboardsConfig.default_allow_all = True

c.DockerSpawner.remove = True

c.DockerSpawner.name_template = "{prefix}-{username}-{servername}"

c.DockerSpawner.image = 'ideonate/containds-allr-scipyr:sha-37a6434'

c.DockerSpawner.pull_policy = 'ifnotpresent'

notebook_dir = '/home/jovyan'
c.DockerSpawner.notebook_dir = notebook_dir
# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir }

c.Spawner.start_timeout = 6000

c.Authenticator.admin_users = {'dan'}

c.ConfigurableHTTPProxy.debug = True

c.JupyterHub.cleanup_servers = True

c.ConfigurableHTTPProxy.should_start = True


import os

#  Generate certs:
# openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout myjupyterhub.net/jupyterhub.key -out myjupyterhub.net/jupyterhub.crt

## Path to SSL certificate file for the public facing interface of the proxy
#
#  When setting this, you should also set ssl_key
c.JupyterHub.ssl_cert = os.environ['SSL_CERT']

## Path to SSL key file for the public facing interface of the proxy
#
#  When setting this, you should also set ssl_cert
c.JupyterHub.ssl_key = os.environ['SSL_KEY']

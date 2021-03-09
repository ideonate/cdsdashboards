import os

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

c.JupyterHub.spawner_class = 'cdsdashboards.hubextension.spawners.variablekube.VariableKubeSpawner'

c.CDSDashboardsConfig.builder_class = 'cdsdashboards.builder.kubebuilder.KubeBuilder'

from jupyter_client.localinterfaces import public_ips

c.JupyterHub.hub_ip = public_ips()[0]

c.KubeSpawner.debug = True


c.CDSDashboardsConfig.show_source_servers = False
c.CDSDashboardsConfig.require_source_server = False

c.CDSDashboardsConfig.default_allow_all = True

c.KubeSpawner.remove = True

c.KubeSpawner.name_template = "{prefix}-{username}-{servername}"

c.KubeSpawner.image = 'ideonate/containds-all-basic:latest'

c.KubeSpawner.pull_policy = 'ifnotpresent'

notebook_dir = '/home/jovyan'
c.KubeSpawner.notebook_dir = notebook_dir
# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container

c.KubeSpawner.pvc_name_template = 'pvc-{username}'

c.KubeSpawner.volumes = [{ 'name': 'jupyterhub-user-{username}', 'persistentVolumeClaim': {notebook_dir} }]

c.KubeSpawner.storage_access_modes = ['ReadWriteMany']
c.KubeSpawner.storage_capacity = '1G'
c.KubeSpawner.storage_pvc_ensure = True

c.KubeSpawner.volumes = [
        {
            'name': 'data',
            'persistentVolumeClaim': {
                'claimName': c.KubeSpawner.pvc_name_template
            }
        }
    ]
c.KubeSpawner.volume_mounts = [
    {
        'mountPath': '/home/jovyan',
        'name': 'data'
    }
]

# User options
if True:
    c.KubeSpawner.profile_list = [
    {
        'display_name': 'Small',
        'slug': 'small',
        'default': True,
        'kubespawner_override': {
            'cpu_limit': 1,
            'mem_limit': '512M'
        }
    }, {
        'display_name': 'Large',
        'slug': 'large',
        'kubespawner_override': {
            'image': 'training/datascience:label',
            'cpu_limit': 1,
            'mem_limit': '1G',
        }
    }]

c.Spawner.start_timeout = 6000

c.Authenticator.admin_users = {'dan'}

c.ConfigurableHTTPProxy.debug = True

c.JupyterHub.cleanup_servers = True

c.ConfigurableHTTPProxy.should_start = True



c.JupyterHub.redirect_to_server = False
c.JupyterHub.default_url = '/hub/dashboards'


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


c.CDSDashboardsConfig.conda_envs = ['env1', 'env2', 'cds']

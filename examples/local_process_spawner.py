# import os


c.JupyterHub.db_url = 'sqlite:///examples/sqlitedbs/local_process_spawner.sqlite'

c.JupyterHub.authenticator_class = 'jupyterhub.auth.DummyAuthenticator'

# # GitHub login trial

# from oauthenticator.github import GitHubOAuthenticator
# c.GitHubOAuthenticator.scope = ['read:org', 'public_repo', 'repo', 'user:email']

# class MyGitHubAuthenticator(GitHubOAuthenticator):
    
#     from tornado import gen

#     @gen.coroutine
#     def pre_spawn_start(self, user, spawner):
#         auth_state = yield user.get_auth_state()
#         import pprint
#         pprint.pprint(auth_state)
#         if not auth_state:
#             # user has no auth state
#             return
#         # define some environment variables from auth_state
#         spawner.environment['GITHUB_TOKEN'] = auth_state['access_token']
#         spawner.environment['GITHUB_USER'] = auth_state['github_user']['login']
#         spawner.environment['GITHUB_EMAIL'] = auth_state['github_user']['email']


# c.JupyterHub.authenticator_class = MyGitHubAuthenticator


# c.GitHubOAuthenticator.enable_auth_state = True

# if 'JUPYTERHUB_CRYPT_KEY' not in os.environ:
#     import warnings

#     warnings.warn(
#         "Need JUPYTERHUB_CRYPT_KEY env for persistent auth_state.\n"
#         "    export JUPYTERHUB_CRYPT_KEY=$(openssl rand -hex 32)"
#     )
#     c.CryptKeeper.keys = [ os.urandom(32) ]
#     c.CryptKeeper.n_threads = 1

# c.CryptKeeper.n_threads = 2


from jupyterhub.spawner import LocalProcessSpawner

class SameUserSpawner(LocalProcessSpawner):

    def make_preexec_fn(self, name):
        return lambda: None

    def user_env(self, env):
        path = '/Users/dan/Dev/cdsdashboards/examples/local_process_folder/%s' % self.user.name

        try:
            os.mkdir(path)
        except OSError:
            print('Failed to create directory: %s' % path)
       
        return env

    def _notebook_dir_default(self):
        return f'/Users/dan/Dev/cdsdashboards/examples/local_process_folder/{self.user.name}'


#    def options_form(self, spawner):
#        self.log.info("In options_form")

#        if spawner.orm_spawner.user_options and 'presentation_type' in spawner.orm_spawner.user_options:
#            return '<p>The PRESENTATION <input type="text" name="v"></input></p>'
#        return '<p>The form <input type="text" name="v"></input></p>'


# c.CDSDashboardsConfig.spawn_default_options = False

from cdsdashboards.hubextension.spawners.variablemixin import VariableMixin, MetaVariableMixin

class VariableSameUserSpawner(SameUserSpawner, VariableMixin, metaclass=MetaVariableMixin):
    pass

c.JupyterHub.spawner_class = VariableSameUserSpawner


c.CDSDashboardsConfig.builder_class = 'cdsdashboards.builder.processbuilder.ProcessBuilder'

c.LocalProcessSpawner.notebook_dir = '/Users/dan/Dev/cdsdashboards/examples/local_process_folder/{username}'

c.Spawner.start_timeout = 6000

c.Spawner.debug = True

c.Authenticator.admin_users = {'dan'}

c.ConfigurableHTTPProxy.debug = True

c.JupyterHub.allow_named_servers = True

import os
dirname = os.path.dirname(__file__)

c.CDSDashboardsConfig.extra_presentation_types = ['plotlydash-debug', 'flask']

c.VariableMixin.extra_presentation_launchers = {
    'plotlydash-debug': {
        'args': [
            'python3', '{presentation_path}', '{port}', '{origin_host}'
            ],
        'env': {
            'PYTHONPATH': os.path.join(dirname, '/Users/dan/Dev/cdsdashboards/examples/local_process_folder/{username}/{presentation_dirname}')
        }
    },
    'flask': {
        'args': ['--destport=0', 'python3', '{-}m','flask_gunicorn_cmd.main', '{presentation_path}',
            '{--}port={port}']
    },
}


c.CDSDashboardsConfig.show_source_git = True
c.CDSDashboardsConfig.show_source_servers = False

c.CDSDashboardsConfig.conda_envs = ['', 'env1', 'env2', 'cds']
#c.CDSDashboardsConfig.allow_custom_conda_env = True

#c.CDSDashboardsConfig.default_allow_all = True

#c.VariableMixin.voila_template = 'materialstream'


#c.CDSDashboardsConfig.spawn_allow_group = 'spawners-group'


c.VariableMixin.proxy_last_activity_interval = 10

c.VariableMixin.proxy_force_alive = True


from cdsdashboards.app import CDS_TEMPLATE_PATHS
from cdsdashboards.hubextension import cds_extra_handlers

c.JupyterHub.template_paths = CDS_TEMPLATE_PATHS
c.JupyterHub.extra_handlers = cds_extra_handlers



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

c.JupyterHub.internal_ssl = False

c.JupyterHub.bind_url = 'https://0.0.0.0:443'

#c.ConfigurableHTTPProxy.command = ['configurable-http-proxy', '--no-x-forward']


c.JupyterHub.redirect_to_server = False

c.JupyterHub.default_url = '/hub/dashboards'

#def default_url_fn(handler):
#    user = handler.current_user
#    if user and user.admin:
#        return '/hub/admin'
#    return '/hub/home'

#c.JupyterHub.default_url = default_url_fn
import os.path
import re
from copy import deepcopy
from traitlets import Unicode, Integer, Dict, Bool
from traitlets.config import Configurable

from jupyterhub.spawner import _quote_safe
from jupyterhub.traitlets import Command

from ..base import SpawnPermissionsController, CDSConfigStore

def _get_voila_template(args, spawner):

    voila_template = getattr(spawner, 'voila_template', '')

    if voila_template != '':
            args.append('='.join(('{--}template', voila_template)))

    return args

def _get_streamlit_debug(args, spawner):
    try:
        if spawner.debug:
            args.insert(args.index('streamlit')+1, '{--}log_level=debug')
    except ValueError:
        pass
    return args

def _fixed_format(s, **kwargs):
    for k,v in kwargs.items():
        s = s.replace(''.join(('{',k,'}')), v)
    return s

class VariableMixin(Configurable):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Merge extra_presentation_launchers config into a copy of builtin_presentation_launchers
        self.merged_presentation_launchers = deepcopy(self.builtin_presentation_launchers)
        for frameworkname, launcher in self.extra_presentation_launchers.items():
            if frameworkname not in self.merged_presentation_launchers:
                self.merged_presentation_launchers[frameworkname] = {}
            for k,v in launcher.items():
                self.merged_presentation_launchers[frameworkname][k] = v

    builtin_presentation_launchers = {
        'voila': {
            #'cmd': ['python3', '-m', 'jhsingle_native_proxy.main'],  # This is the default cmd anyway
            'args': ['--destport=0', 'python3', '{-}m','voila', '{presentation_path}',
                '{--}port={port}',
                '{--}no-browser',
                '{--}Voila.base_url={base_url}/',
                '{--}Voila.server_url=/'],
            'extra_args_fn': _get_voila_template
        },
        'streamlit': {
            'args': ['--destport=0', 'streamlit', 'run', '{presentation_path}', 
                '{--}server.port={port}',
                '{--}server.headless=True',
                '{--}browser.serverAddress={origin_host}',
                '{--}browser.gatherUsageStats=false'],
            'debug_args': [], # The default is {--}debug, we don't want that
            'extra_args_fn': _get_streamlit_debug # But --log_level=debug has to come earlier in the cmdline
        },
        'plotlydash': {
            'args': ['--destport=0', 'python3', '{-}m','plotlydash_tornado_cmd.main', '{presentation_path}',
                '{--}port={port}'],
            'env': {'DASH_REQUESTS_PATHNAME_PREFIX': '{base_url}/'}
        },
        'bokeh': {
            'args': ['--destport=0', 'python3', '{-}m','bokeh_root_cmd.main', '{presentation_path}',
                '{--}port={port}',
                '{--}allow-websocket-origin={origin_host}',
                '--ready-check-path=/ready-check']
        },
        'rshiny': {
            'args': ['--destport=0', 'python3', '{-}m','rshiny_server_cmd.main', '{presentation_path}',
                '{--}port={port}']
        }

    }

    extra_presentation_launchers = Dict(
        {},
        help="""
        Configuration dict containing details of any custom frameworks that should be made available to Dashboard creators.
        Any new keys added here also need to be added to the c.CDSDashboardsConfig.presentation_types list.
        See cdsdashboards/hubextension/spawners/variablemixin.py in the https://github.com/ideonate/cdsdashboards source code
        for details of the builtin_presentation_launchers dict which shows some examples. This extra_presentation_launchers 
        config takes the same format.
        Any keys in extra_presentation_launchersthat also belong to builtin_presentation_launchers will be merged into the 
        builtin config, e.g. {'streamlit':{'env':{'STREAMLIT_ENV_VAR':'TEST'}}} will overwrite only the env section of the 
        builting streamlit launcher.
        """
    ).tag(config=True)

    default_presentation_cmd = Command(
        ['python3', '-m', 'jhsingle_native_proxy.main'],
        allow_none=False,
        help="""
        The command to run presentations through jhsingle_native_proxy, can be a string or list.
        Default is ['python3', '-m', 'jhsingle_native_proxy.main']
        Change to e.g. ['start.sh', 'python3', '-m', 'jhsingle_native_proxy.main'] to ensure start hooks are
        run in the singleuser Docker images.
        """
    ).tag(config=True)

    voila_template = Unicode(
        '',
        help="""
        --template argument to pass to Voila. Default is blank (empty string) to not pass any template to Voila command line.
        """,
    ).tag(config=True)

    proxy_request_timeout = Integer(
        0,
        help="""
        Request timeout in seconds that jhsingle-native-proxy should allow when proxying to the underlying process (e.g. Voila).
        The default of 0 means that no --request-timeout flag will be passed to jhsingle-native-proxy so it will use its own default.
        """,
    ).tag(config=True)

    proxy_force_alive = Bool(
        True,
        help="""
        Whether or not jhsingle-native-proxy should fake activity on its subprocess, always reporting to the hub that activity has happened.
        The default of True means that no flag will be passed to jhsingle-native-proxy so it will use its own default (expected to be --force-alive).
        If False is specified, --no-force-alive will be passed to jhsingle-native-proxy.
        """,
    ).tag(config=True)

    proxy_last_activity_interval = Integer(
        300,
        help="""
        Frequency in seconds that jhsingle-native-proxy should send any recent activity timestamp to the hub.
        If the default of 300 is specified, no --last-activity-interval flag will be passed to jhsingle-native-proxy so it will use its default.
        Otherwise the specified value will be passed to --last-activity-interval.
        """,
    ).tag(config=True)

    async def start(self):
        """
        Copy trait values from user_options into the trait attrs of the spawner object
        """

        if self.user_options:
            trait_names = set(self.trait_names()) - {'user_options'}
            for k in trait_names.intersection(self.user_options.keys()):
                merged_trait = self.user_options[k]
                if type(getattr(self, k, None)) == dict:
                    # Merge dicts if one already exists for this trait
                    merged_trait = {**getattr(self, k), **merged_trait}
                setattr(self, k, merged_trait)

        # Any update for cmd needs to be set here (args and env have their own overridden functions)
        presentation_type = self._get_presentation_type()
        if presentation_type != '':
            launcher = self.merged_presentation_launchers[presentation_type]
            if 'cmd' in launcher:
                self.cmd = launcher['cmd']
            else:
                self.cmd = self.default_presentation_cmd

        return await super().start()

    def get_args(self):
        """Return the arguments to be passed after self.cmd

        Doesn't expect shell expansion to happen.

        Also adds self.args at the end in case specified by the config.
        """

        presentation_type = self._get_presentation_type()
        
        if presentation_type == '':
            return super().get_args()

        launcher = self.merged_presentation_launchers[presentation_type]

        presentation_path = self.user_options.get('presentation_path', '')

        args = []

        # jhsingle-native-proxy --destport $destport --authtype oauth voila `pwd` {--}port={port} {--}no-browser {--}Voila.base_url={base_url}/ {--}Voila.server_url=/ --port $port

        notebook_dir = '.'
        if self.notebook_dir:
            notebook_dir = self.format_string(self.notebook_dir)

        git_repo = self.user_options.get('git_repo', '')
        repofolder = ''
        if git_repo != '':
            repofolder = self._calc_repo_folder(git_repo)
            args.append('--repo={}'.format(_quote_safe(git_repo)))
            notebook_dir = os.path.join(notebook_dir, repofolder)
            args.append('--repofolder={}'.format(_quote_safe(notebook_dir)))

        if presentation_path != '' and not '..' in presentation_path:
            # Should have been validated when dashboard created, but .. is particularly dangerous
            presentation_path = re.sub('^/+', '', presentation_path) # Remove leading slash(es) to ensure it is relative to home folder
            notebook_dir = os.path.join(notebook_dir, presentation_path)

        if 'args' in launcher:
            args.extend(launcher['args'])

        args.append('--presentation-path={}'.format(_quote_safe(notebook_dir)))

        conda_env = self.user_options.get('conda_env', '')
        if conda_env != '':
            args.append('--conda-env=%s' % _quote_safe(conda_env))

        if self.ip:
            args.append('--ip=%s' % _quote_safe(self.ip))

        if self.port:
            args.append('--port=%i' % self.port)

        if self.debug:
            if 'debug_args' in launcher:
                args.extend(launcher['debug_args'])
            else:
                args.append('{--}debug')
            args.append('--debug') # For jhsingle-native-proxy itself

        proxy_request_timeout = getattr(self, 'proxy_request_timeout', 0)
        if proxy_request_timeout:
            args.append('--request-timeout={}'.format(proxy_request_timeout))

        proxy_force_alive = getattr(self, 'proxy_force_alive', True)
        if proxy_force_alive == False:
            args.append('--no-force-alive')

        proxy_last_activity_interval = getattr(self, 'proxy_last_activity_interval', 300)
        if proxy_last_activity_interval != 300:
            args.append('--last-activity-interval={}'.format(proxy_last_activity_interval))

        args.extend(self.args)

        if 'extra_args_fn' in launcher and callable(launcher['extra_args_fn']): # Last chance for launcher config to change everything and anything
            args = launcher['extra_args_fn'](args, self)

        return args

    def _get_presentation_type(self):
        """
        Returns the presentation_type (e.g. '' for standard spawner, 'voila', 'streamlit' for named presentation frameworks).
        Throws an exception if the presentation_type doesn't have a launcher configuration in either extra_presentation_launchers 
        or builtin_presentation_launchers.
        """
        if self.user_options and 'presentation_type' in self.user_options:
            presentation_type = self.user_options['presentation_type']
            if presentation_type not in self.merged_presentation_launchers:
                raise Exception('presentation type {} has not been registered with the spawner'.format(presentation_type))
            return presentation_type
        return ''

    def get_env(self):
        env = super().get_env()

        presentation_type = self._get_presentation_type()

        if presentation_type != '':

            launcher = self.merged_presentation_launchers[presentation_type]

            if 'env' in launcher:
                presentation_dirname = '.'
                presentation_path = ''
                if self.user_options and 'presentation_path' in self.user_options:
                    presentation_path = self.user_options['presentation_path']
                    presentation_dirname = os.path.dirname(presentation_path)

                self.log.info('presentation_dirname: {}'.format(presentation_dirname))

                for k,v in launcher['env'].items():
                    env[k] = _fixed_format(v, 
                        base_url=self.server.base_url,
                        presentation_dirname=presentation_dirname,
                        presentation_path=presentation_path,
                        username=self.user.name
                    )
        return env

    def _calc_repo_folder(self, git_repo):
        s = re.sub('^https?', '', git_repo.lower()) # Remove https and convert to lower case
        s = re.sub('[^a-z0-9]', '-', s) # Replace any non-alphanumeric chars with dash
        s = re.sub('^-+|-+$|-(?=-)', '', s) # Remove dashes from start/end and reduce multiple dashes to just one dash
        return s

    def run_pre_spawn_hook(self):
        if not SpawnPermissionsController.get_instance(CDSConfigStore.get_instance(self.config), self.db).can_user_spawn(self.user.orm_user):
            raise Exception('User {} is not allowed to spawn a server'.format(self.user.name))
        return super().run_pre_spawn_hook()


class MetaVariableMixin(type(Configurable)):
    """
    Use this metaclass to ensure VariableMixin occurs earlier in the MRO, so all traits are accessible at the right time.
    """
    
    def mro(cls):
        mro = super().mro()
        # Take VariableMixin (normally item 4) and put it at item 1
        try:
            vm_index = mro.index(VariableMixin)
            if vm_index > 1 and vm_index < len(mro)-1:
                mro = [mro[0], mro[vm_index]]+ mro[1:vm_index] + mro[vm_index+1:]
        except ValueError:
            pass
        
        return mro

import os.path
from traitlets import Unicode, Integer
from traitlets.config import Configurable

from jupyterhub.spawner import _quote_safe


class VariableMixin(Configurable):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    voila_template = Unicode(
        'materialstream',
        help="""
        --template argument to pass to Voila. Default is materialstream
        """,
    ).tag(config=True)

    proxy_request_timeout = Integer(
        0,
        help="""
        Request timeout in seconds that jhsingle-native-proxy should allow when proxying to the underlying process (e.g. Voila).
        The default of 0 means that no --request-timeout flag will be passed to jhsingle-native-proxy so it will use its own default.
        """,
    ).tag(config=True)

    async def start(self):
        """
        Copy trait values from user_options into the trait attrs of the spawner object
        """

        if self.user_options:
            trait_names = set(self.trait_names()) - {'user_options'}
            for k in trait_names.intersection(self.user_options.keys()):
                setattr(self, k, self.user_options[k])

        return await super().start()

    def get_args(self):
        """Return the arguments to be passed after self.cmd

        Doesn't expect shell expansion to happen.

        Also adds self.args at the end in case specified by the config.
        """

        presentation_type = self._get_presentation_type()
        
        if presentation_type == '':
            return super().get_args()

        presentation_path = self.user_options.get('presentation_path', '')

        args = ['--destport=0']

        # jhsingle-native-proxy --destport $destport --authtype oauth voila `pwd` {--}port={port} {--}no-browser {--}Voila.base_url={base_url}/ {--}Voila.server_url=/ --port $port

        if self.ip:
            args.append('--ip=%s' % _quote_safe(self.ip))

        if self.port:
            args.append('--port=%i' % self.port)


        notebook_dir = '.'
        if self.notebook_dir:
            notebook_dir = self.format_string(self.notebook_dir)

        if presentation_path != '' and not '..' in presentation_path:
            # Should have been validated when dashboard created, but .. is particularly dangerous
            if presentation_path.startswith("/"):
                presentation_path = presentation_path[1:]
            notebook_dir = os.path.join(notebook_dir, presentation_path)


        voila_template = getattr(self, 'voila_template', '')

        if presentation_type == 'voila':

            args.extend(['python3', '{-}m','voila'])

            args.append(_quote_safe(notebook_dir))

            args.extend([
                '{--}port={port}',
                '{--}no-browser',
                '{--}Voila.base_url={base_url}/',
                '{--}Voila.server_url=/'
            ])

            if voila_template != '':
                args.append('='.join(('{--}template', voila_template)))

            if self.debug:
                args.append('{--}debug')

        elif presentation_type == 'streamlit':

            args.append('streamlit')

            if self.debug:
                args.append('{--}log_level=debug')

            args.append('run')

            args.append(_quote_safe(notebook_dir))

            args.extend([
                '{--}server.port={port}',
                '{--}server.headless=True',
                '{--}server.enableCORS=False'
            ])

            
        elif presentation_type == 'plotlydash':

            args.extend(['python3', '{-}m','plotlydash_tornado_cmd.main'])

            args.append(_quote_safe(notebook_dir))

            args.extend([
                '{--}port={port}'
            ])

            if self.debug:
                args.append('{--}debug')


        elif presentation_type == 'bokeh':

            args.extend(['python3', '{-}m','bokeh_root_cmd.main'])

            args.append(_quote_safe(notebook_dir))

            args.extend([
                '{--}port={port}',
                '{--}allow-websocket-origin={origin_host}'
            ])

            if self.debug:
                args.append('{--}debug')

        elif presentation_type == 'rshiny':

            args.extend(['python3', '{-}m','rshiny_server_cmd.main'])

            args.append(_quote_safe(notebook_dir))

            args.extend([
                '{--}port={port}'
            ])

            if self.debug:
                args.append('{--}debug')


        if self.debug:
            # jhsingle-native-proxy debug
            args.append('--debug')

        proxy_request_timeout = getattr(self, 'proxy_request_timeout', 0)
        if proxy_request_timeout:
            args.append('--request-timeout={}'.format(proxy_request_timeout))

        args.extend(self.args)
        return args

    def _get_presentation_type(self):
        if self.user_options and 'presentation_type' in self.user_options:
            return self.user_options['presentation_type']
        return ''

    def get_env(self):
        env = super().get_env()

        presentation_type = self._get_presentation_type()

        if presentation_type == 'plotlydash':
            env['DASH_REQUESTS_PATHNAME_PREFIX'] = "{}/".format(self.server.base_url)
        return env


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

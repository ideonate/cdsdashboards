import os.path

from traitlets import Unicode

from jupyterhub.spawner import LocalProcessSpawner, _quote_safe


class VariableLocalProcessSpawner(LocalProcessSpawner):

    presentation_type = Unicode(
        '',
        help="""
        Whether to run as voila ('voila') or regular jupyterhub singleuser ('')
        """,
    ).tag(config=True)

    presentation_path = Unicode(
        '',
        help="""
        Any specific file or folder to run in voila
        """,
    ).tag(config=True)

    voila_template = Unicode(
        'materialstream',
        help="""
        --template argument to pass to Voila. Default is materialstream
        """,
    ).tag(config=True)

    async def start(self):
        if self.user_options:
            # TODO whitelist permitted options
            for k,v in self.user_options.items():
                setattr(self, k, v)

        return await super().start()

    def get_args(self):
        """Return the arguments to be passed after self.cmd

        Doesn't expect shell expansion to happen.
        """

        if self.presentation_type == '':
            return super().get_args()

        args = ['--destport=0']

        # jhsingle-native-proxy --destport $destport --authtype oauth voila `pwd` {--}port={port} {--}no-browser {--}Voila.base_url={base_url}/ {--}Voila.server_url=/ --port $port


        if self.ip:
            args.append('--ip=%s' % _quote_safe(self.ip))

        if self.port:
            args.append('--port=%i' % self.port)

        args.append('voila')

        notebook_dir = ''
        if self.notebook_dir:
            notebook_dir = self.format_string(self.notebook_dir)
        else:
            notebook_dir = '`pwd`' # TODO Change this

        if self.presentation_path != '' and not '..' in self.presentation_path:
            # Should have been validated when dashboard created, but .. is particularly dangerous
            presentation_path = self.presentation_path
            if presentation_path.startswith("/"):
                presentation_path = presentation_path[1:]
            notebook_dir = os.path.join(notebook_dir, presentation_path)

        args.append(_quote_safe(notebook_dir))

        args.append('{--}port={port}')

        args.append('{--}no-browser')

        args.append('{--}Voila.base_url={base_url}/')
        args.append('{--}Voila.server_url=/')

        template = self.voila_template
        if template != '':
            args.append('='.join(('{--}template', template)))

        #if self.default_url:
        #    default_url = self.format_string(self.default_url)
        #    args.append('--NotebookApp.default_url=%s' % _quote_safe(default_url))

        if self.debug:
            args.append('--debug')
        #if self.disable_user_config:
        #    args.append('--disable-user-config')
        args.extend(self.args)
        return args

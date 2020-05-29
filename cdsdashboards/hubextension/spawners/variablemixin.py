import os.path

from jupyterhub.spawner import _quote_safe


class VariableMixin():

    def _pre_start(self):
        if self.user_options:
            trait_names = set(self.trait_names()) - {'user_options'}
            for k in trait_names.intersection(self.user_options.keys()):
                setattr(self, k, self.user_options[k])

    def _mixin_get_args(self, presentation_type):
        """Return the arguments to be passed after self.cmd

        Doesn't expect shell expansion to happen.

        Also adds self.args at the end in case specified by the config.
        """

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

            args.extend(['streamlit', 'run'])

            args.append(_quote_safe(notebook_dir))

            args.extend([
                '{--}server.port={port}',
                '{--}server.headless=True',
                '{--}server.enableCORS=False'
            ])

            if self.debug:
                args.append('{--}log_level=debug')

        if self.debug:
            # jhsingle-native-proxy debug
            args.append('--debug')

        args.extend(self.args)
        return args


from systemdspawner import SystemdSpawner
from traitlets import Unicode

from .variablemixin import VariableMixin


class VariableSystemdSpawner(SystemdSpawner, VariableMixin):

    voila_template = Unicode(
        '',
        help="""
        --template argument to pass to Voila. Default is materialstream
        """,
    ).tag(config=True)

    async def start(self):
        self._pre_start()
        return await super().start()

    def get_args(self):
        presentation_type = ''

        if self.user_options and 'presentation_type' in self.user_options:
            presentation_type = self.user_options['presentation_type']
        
        if presentation_type == '':
            return super().get_args()

        return self._mixin_get_args(presentation_type)


from systemdspawner import SystemdSpawner
from traitlets import Unicode

from .variablemixin import VariableMixin


class VariableSystemdSpawner(SystemdSpawner, VariableMixin):

    voila_template = Unicode(
        'materialstream',
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

    def _expand_user_vars(self, string):
        """
        Expand user related variables in a given string

        Currently expands:
          {USERNAME} -> Name of the user
          {USERID} -> UserID
          {SERVERNAMESU} -> Server Name (or 'singleuser' if server is My Server which has no name)
          Note use of {SERVERNAMESU} could cause conflict if a named server is named 'singleuser'...
          Also needs to preserve --, port, and base_url to pass on to jhsingle-native-proxy
        """
        return string.replace('{USERNAME}', self.user.name).replace('{USERID}', str(self.user.id)).replace('{SERVERNAMESU}', self.name or 'singleuser')


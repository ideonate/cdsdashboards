from systemdspawner import SystemdSpawner

from .variablemixin import VariableMixin, MetaVariableMixin


class VariableSystemdSpawner(SystemdSpawner, VariableMixin, metaclass=MetaVariableMixin):

    def _expand_user_vars(self, string):
        """
        Expand user related variables in a given string

        Currently expands:
          {USERNAME} -> Name of the user
          {USERID} -> UserID
          {DASHSERVERNAME} -> A Dash plus Server Name (or '' if server is My Server which has no name)
          Also needs to preserve --, port, and base_url to pass on to jhsingle-native-proxy, so don't use straight format function
        """
        dsn = ''
        if self.name:
            dsn = '-{}'.format(self.name)
        return string.replace('{USERNAME}', self.user.name).replace('{USERID}', str(self.user.id)).replace('{DASHSERVERNAME}', dsn)


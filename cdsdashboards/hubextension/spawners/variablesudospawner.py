import json
import os
import getpass
import shutil
import sys

from sudospawner import SudoSpawner
from traitlets import Unicode

from .variablemixin import VariableMixin, MetaVariableMixin
from sudospawner.mediator import spawn, kill
from tornado.options import parse_command_line
from tornado import log
app_log = log.app_log

class VariableSudoSpawner(SudoSpawner, VariableMixin, metaclass=MetaVariableMixin):

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
            self.sudospawner_path = shutil.which('cds_sudospawner') or 'cds_sudospawner'
            launcher = self.merged_presentation_launchers[presentation_type]
            if 'cmd' in launcher:
                self.cmd = launcher['cmd']
            else:
                self.cmd = self.default_presentation_cmd

        return await super().start()


def mediator(*args, **kwargs):
    parse_command_line()
    app_log.debug("Starting mediator for %s", getpass.getuser())
    try:
        kwargs = json.load(sys.stdin)
    except ValueError as e:
        app_log.error("Expected JSON on stdin, got %s" % e)
        sys.exit(1)

    action = kwargs.pop('action')
    if action == 'kill':
        kill(**kwargs)
    elif action == 'spawn':
        spawn("jhsingle-native-proxy", **kwargs)
    else:
        raise TypeError("action must be 'spawn' or 'kill'")
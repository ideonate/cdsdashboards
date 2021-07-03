from traitlets import default
from kubespawner import KubeSpawner

from .variablemixin import VariableMixin, MetaVariableMixin, Command


class VariableKubeSpawner(KubeSpawner, VariableMixin, metaclass=MetaVariableMixin):

    default_presentation_cmd = Command(
        ['start.sh', 'python3', '-m', 'jhsingle_native_proxy.main'],
        allow_none=False,
        help="""
        The command to run presentations through jhsingle_native_proxy, can be a string or list.
        Default is ['python3', '-m', 'jhsingle_native_proxy.main']
        Change to e.g. ['start.sh', 'python3', '-m', 'jhsingle_native_proxy.main'] to ensure start hooks are
        run in the singleuser Docker images.
        """
    ).tag(config=True)
    
    @default("options_from_form")
    def _options_from_form_default(self):
        """
        Make sure we wrap the default options_from_form in a function that will preserve dashboard metadata
        May need to override this to something more specific, e.g. in KubeSpawner
        """
        usefn = self._default_options_from_form  # Spawner class default, just in case
        if hasattr(self, "_options_from_form"):  # KubeSpawner >= 1.0
            usefn = self._options_from_form
        elif hasattr(self, "options_from_form"):  # KubeSpawner < 1.0, although options_from_form fn will override this default anyway
            usefn = self.options_from_form

        return self._wrap_options_from_form(usefn)

    def get_env(self):
        """Return the environment dict to use for the Spawner.
        See also: jupyterhub.Spawner.get_env
        """

        env = super().get_env()
        # Add environment variables from user_options
        extra_env = self.user_options.get('environment', None)
        if extra_env is None:
            self.log.warning("No extra environment variables found in user_options for VariableKubeSpawner!")
        if not isinstance(extra_env, dict):
            self.log.warning("Error: `environment` user_option for VariableKubeSpawner is not a dictionary, but a {}"
                             .format(type(extra_env)))
        for key, val in extra_env.items():
            env[key] = val

        return env

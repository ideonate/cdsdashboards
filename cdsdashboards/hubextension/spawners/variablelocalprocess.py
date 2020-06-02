from jupyterhub.spawner import LocalProcessSpawner
from traitlets import Unicode, Integer

from .variablemixin import VariableMixin


class VariableLocalProcessSpawner(LocalProcessSpawner, VariableMixin):
    
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
        self._pre_start()
        return await super().start()

    def get_args(self):
        presentation_type = self._get_presentation_type()
        
        if presentation_type == '':
            return super().get_args()

        return self._mixin_get_args(presentation_type)

    def get_env(self):
        env = super().get_env()

        presentation_type = self._get_presentation_type()

        if presentation_type != '':
            env = self._mixin_get_env(env, presentation_type)

        return env

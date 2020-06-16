from jupyterhub.spawner import LocalProcessSpawner

from .variablemixin import VariableMixin, MetaVariableMixin


class VariableLocalProcessSpawner(LocalProcessSpawner, VariableMixin, metaclass=MetaVariableMixin):
    pass


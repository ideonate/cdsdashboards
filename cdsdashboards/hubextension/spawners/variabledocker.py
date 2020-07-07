from dockerspawner import DockerSpawner, SwarmSpawner, SystemUserSpawner

from .variablemixin import VariableMixin, MetaVariableMixin


class VariableDockerSpawner(DockerSpawner, VariableMixin, metaclass=MetaVariableMixin):
    
    pass


class VariableSwarmSpawner(SwarmSpawner, VariableMixin, metaclass=MetaVariableMixin):
    
    pass


class VariableSystemUserSpawner(SystemUserSpawner, VariableMixin, metaclass=MetaVariableMixin):
    
    pass

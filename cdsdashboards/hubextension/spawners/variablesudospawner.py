from sudospawner import SudoSpawner

from .variablemixin import VariableMixin, MetaVariableMixin


class VariableSudoSpawner(SudoSpawner, VariableMixin, metaclass=MetaVariableMixin):
    pass

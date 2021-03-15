.. _batchspawners:


BatchSpawners
=============

If your JupyterHub is using a `BatchSpawner <https://github.com/jupyterhub/batchspawner>`__ then please broadly follow 
the setup instructions for :ref:`localprocess`.

However, you will need to define a custom spawner class in your jupyterhub_config.py file.

For example, if you are using SlurmSpawner:

::

    from batchspawner import SlurmSpawner
    from cdsdashboards.hubextension.spawners.variablemixin import VariableMixin, MetaVariableMixin

    class VariableSlurmSpawner(SlurmSpawner, VariableMixin, metaclass=MetaVariableMixin):
        pass

    c.JupyterHub.spawner_class = VariableSlurmSpawner


    c.VariableMixin.default_presentation_cmd = ['jhsingle-native-proxy']


The final line is normally required in order to navigate through the way the standard 
`batchspawner-singleuser <https://github.com/jupyterhub/batchspawner/blob/master/batchspawner/singleuser.py>`__ script works.
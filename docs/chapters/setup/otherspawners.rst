.. _otherspawners:

Other Spawners
==============

It should be possible to adapt most JupyterHub spawner types to work with ContainDS Dashboards. The most important 
thing is to ensure it responds correctly when run with a 'cmd' of :code:`python -m jhsingle_native_proxy.main` 
instead of :code:`jupyterhub-singleuser`.

Popular spawners such as KubeSpawner, LocalProcessSpawner, SystemdSpawner, DockerSpawner, and the UserCreatingSpawner 
that comes with The Littlest JupyterHub already have 'Variable' versions provided with the cdsdashboards package.

The various BatchSpawners and SudoSpawner are described below.

In general, take a look at the documentation for installing ContainDS Dashboards with a spawner that is similar to 
the one you want to use, then create your own spawner in jupyterhub_config.py as follows (using 'MySpawner' as an 
example):

::

    from cdsdashboards.hubextension.spawners.variablemixin import VariableMixin, MetaVariableMixin

    class VariableMySpawner(MySpawner, VariableMixin, metaclass=MetaVariableMixin):
        pass

    c.JupyterHub.spawner_class = VariableMySpawner


BatchSpawners
-------------

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


SudoSpawner
-----------

A variable version of SudoSpawner is provided within cdsdashboards. You should probably follow the instructions for 
:ref:`localprocess` except use this for the spawner_class:

::

    c.JupyterHub.spawner_class = 'cdsdashboards.hubextension.spawners.variablesudospawner.VariableSudoSpawner'


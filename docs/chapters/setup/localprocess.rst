.. _localprocess:


LocalProcessSpawner or SystemdSpawner
=====================================

JupyterHub's default spawner (method of starting new Jupyter environments for individual users) is called 
`LocalProcessSpawner <https://jupyterhub.readthedocs.io/en/stable/api/spawner.html#localprocessspawner>`__. 
It simply runs 'jupyter notebook' as a new process on the server.

`SystemdSpawner <https://github.com/jupyterhub/systemdspawner>`__ is very similar but offers tighter control over the processes being 
run since it uses systemd, a system and service manager.

If in doubt, just start with LocalProcessSpawner then move on to SystemdSpawner if needed. 
If using The Littlest JupyterHub, SystemdSpawner is the default.

Note that you may have two different Python environments: the 'hub' environment and the 'user' environment. The hub environment is where 
JupyterHub itself is running, serving the main web framework for login and managing Jupyter servers on your JupyterHub website. The user 
environment is where individual's Jupyter notebooks are running.

For example, in The Littlest JupyterHub, the two environments are usually located in /opt/tljh/hub (for the hub environment) and /opt/tljh/user 
(for the user environment).

Installing cdsdashboards
~~~~~~~~~~~~~~~~~~~~~~~~

Install the cdsdashboards package in the hub environment:

::

    pip install cdsdashboards


Also install in the user environment:

::

    pip install cdsdashboards


Not all dependencies are strictly required in both environments - work is underway to split these out into separate installation tracks.

The key package for the hub environment is cdsdashboards itself; for the user environment the crucial package is jhsingle-native-proxy as well 
as the 'presentation package' - Voila, which is a user-friendly and safe way to display Jupyter notebooks to non-technical users.

Changes to jupyterhub_config.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Change or add the following in your jupyterhub_config.py file.

::

    # Replacement for LocalProcessSpawner
    c.JupyterHub.spawner_class = 'cdsdashboards.hubextension.spawners.VariableLocalProcessSpawner'

    # OR...

    # Replacement for SystemdSpawner
    #c.JupyterHub.spawner_class = 'cdsdashboards.hubextension.spawners.VariableSystemdSpawner'

    # OR...

    # Replacement for UserCreatingSpawner (a simple extension of SystemdSpawner) - The Littlest JupyterHub's default spawner
    #c.JupyterHub.spawner_class = 'cdsdashboards.hubextension.spawners.variableusercreating.VariableUserCreatingSpawner'


    c.JupyterHub.allow_named_servers = True

    c.CDSDashboardsConfig.builder_class = 'cdsdashboards.builder.processbuilder.ProcessBuilder'

    from cdsdashboards.app import CDS_TEMPLATE_PATHS
    from cdsdashboards.hubextension import cds_extra_handlers

    c.JupyterHub.template_paths = CDS_TEMPLATE_PATHS
    c.JupyterHub.extra_handlers = cds_extra_handlers


The allow_named_servers option is a standard JupyterHub option where every user gets more than just their single 'My Server' Jupyter environment. 
They can add extra environments by specifying a name. ContainDS Dashboards makes use of this by running the presentation servers as named servers - 
they are really servers just like the original Jupyter notebook servers, but running Voila or another system instead.

Instead of the original LocalProcessSpawner, you actually need to use a slightly enhanced version of that spawner called VariableLocalProcessSpawner 
- that is set by assigning to c.JupyterHub.spawner_class as above. 
If using SystemdSpawner, comment out the line containing VariableSystemdSpawner instead.
VariableUserCreatingSpawner should be used in a default The Littlest JupyterHub (TLJH) installation.

If you are using TLJH, you can copy the settings above into a new file called 
/opt/tljh/config/jupyterhub_config.d/cdsdashboards_config.py, although ideally you would set allow_named_servers and spawner_class through 
tljh-config (but that doesn't matter if you're just trying it out).

Options
~~~~~~~

Extra options to control behavior of Dashboards are available - see :ref:`options<options>`.

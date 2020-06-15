.. _localprocess:


LocalProcessSpawner or SystemdSpawner
=====================================

JupyterHub's default spawner (method of starting new Jupyter environments for individual users) is called 
`LocalProcessSpawner <https://jupyterhub.readthedocs.io/en/stable/api/spawner.html#localprocessspawner>`__. 
It simply runs 'jupyter notebook' as a new process on the server.

`SystemdSpawner <https://github.com/jupyterhub/systemdspawner>`__ is very similar but offers tighter control over the processes being 
run since it uses systemd, a system and service manager.

If you are using The Littlest JupyterHub - a nice simple distribution that will get you started on a single server - please 
:ref:`see specific TLJH instructions<tljh>`.

Note that you may have two different Python environments: the 'hub' environment and the 'user' environment. The hub environment is where 
JupyterHub itself is running, serving the main web framework for login and managing Jupyter servers on your JupyterHub website. The user 
environment is where individual's Jupyter notebooks are running.


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

If you plan to make use of Streamlit dashboards, also :code:`pip install streamlit` in the user environment. 
For Plotly Dash, also run :code:`pip install dash`.

Changes to jupyterhub_config.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Change or add the following in your jupyterhub_config.py file.

**NOTE: you need to choose one of the two first sections below depending on whether you are using SystemdSpawner or LocalProcessSpawner - 
comment or delete the other.**

::

    # Replacement for LocalProcessSpawner
    c.JupyterHub.spawner_class = 'cdsdashboards.hubextension.spawners.VariableLocalProcessSpawner'

    # OR...

    # Replacement for SystemdSpawner
    #c.JupyterHub.spawner_class = 'cdsdashboards.hubextension.spawners.variablesystemd.VariableSystemdSpawner'
    #c.SystemdSpawner.unit_name_template = 'jupyter-{USERNAME}{DASHSERVERNAME}'

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

If using SystemdSpawner, comment out the line containing VariableSystemdSpawner instead, and the unit_name_template line beneath it. 
At the time of writing, the default SystemdSpawner does not work correctly with 
named servers, and a workaround is provided through VariableUserCreatingSpawner and a new unit_name_template, as seen above. This may 
not be consistent with your existing unit names.


Options
~~~~~~~

Extra options to control behavior of Dashboards are available - see :ref:`options<options>`.

Please `sign up to the ContainDS email list <https://containds.com/signup/>`__ to receive notifications about updates to the project including new 
features and security advice.

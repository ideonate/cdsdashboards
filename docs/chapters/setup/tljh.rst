.. _tljh:


The Littlest JupyterHub
=======================

There is a nice easy distribution of JupyterHub that is a great way to get started on a single-server computer.

These instructions take you through setting up ContainDS Dashboards on a standard install of The Littlest JupyterHub (TLJH).

First of all, `set up your TLJH <http://tljh.jupyter.org/en/latest/install/index.html>`__ - on the cloud, in your own server, 
or just on a laptop in a VM.


Python environments
~~~~~~~~~~~~~~~~~~~

Note that you may have two different Python environments: the 'hub' environment and the 'user' environment. The hub environment is where 
JupyterHub itself is running, serving the main web framework for login and managing Jupyter servers on your JupyterHub website. The user 
environment is where individual's Jupyter notebooks are running.

For example, in The Littlest JupyterHub, the two environments are usually located in /opt/tljh/hub (for the hub environment) and /opt/tljh/user 
(for the user environment).

Installing cdsdashboards
~~~~~~~~~~~~~~~~~~~~~~~~

Install the cdsdashboards package in the hub environment:

::

    sudo -E /opt/tljh/hub/bin/python3 -m pip install cdsdashboards


Also install in the user environment:

::

    sudo -E /opt/tljh/user/bin/python3 -m pip install cdsdashboards


Not all dependencies are strictly required in both environments - work is underway to split these out into separate installation tracks.

The key package for the hub environment is cdsdashboards itself; for the user environment the crucial package is jhsingle-native-proxy as well 
as the 'presentation package' - Voila, which is a user-friendly and safe way to display Jupyter notebooks to non-technical users.

Changes to jupyterhub_config.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Change or add the following in your JupyterHub config.

You can copy the settings above into a new file called 
/opt/tljh/config/jupyterhub_config.d/cdsdashboards_config.py, although ideally you would set allow_named_servers and spawner_class through 
tljh-config (but that doesn't matter if you're just trying it out).

::

    # Replacement for UserCreatingSpawner (a simple extension of SystemdSpawner) - The Littlest JupyterHub's default spawner
    c.JupyterHub.spawner_class = 'cdsdashboards.hubextension.spawners.variableusercreating.VariableUserCreatingSpawner'

    c.SystemdSpawner.unit_name_template = 'jupyter-{USERNAME}{DASHSERVERNAME}'

    c.JupyterHub.allow_named_servers = True

    c.CDSDashboardsConfig.builder_class = 'cdsdashboards.builder.processbuilder.ProcessBuilder'

    from cdsdashboards.app import CDS_TEMPLATE_PATHS
    from cdsdashboards.hubextension import cds_extra_handlers

    c.JupyterHub.template_paths = CDS_TEMPLATE_PATHS
    c.JupyterHub.extra_handlers = cds_extra_handlers


The allow_named_servers option is a standard JupyterHub option where every user gets more than just their single 'My Server' Jupyter environment. 
They can add extra environments by specifying a name. ContainDS Dashboards makes use of this by running the presentation servers as named servers - 
they are really servers just like the original Jupyter notebook servers, but running Voila or another system instead.

Instead of the original UserCreatingSpawner, you actually need to use a slightly enhanced version of that spawner called  
- that is set by assigning to c.JupyterHub.spawner_class as above. At the time of writing, the default SystemdSpawner does not work correctly with 
named servers, and a workaround is provided through VariableUserCreatingSpawner and a new unit_name_template, as seen above.

Reload the TLJH servers:

::

    sudo tljh-config reload


If you find that Dashboards end up giving a 404 not found error (and named servers created on the Home page also do) 
please see :ref:`tljh-named-servers-show-404-not-found`.

Options
~~~~~~~

Extra options to control behavior of Dashboards are available - see :ref:`options<options>`.

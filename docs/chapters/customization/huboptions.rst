.. _huboptions:


Hub Options
-----------

There are extra options that can be added to your jupyterhub_config.py file. 
(See `here <http://tljh.jupyter.org/en/latest/topic/escape-hatch.html>`__ for how to add config on The Littlest JupyterHub.)

Named Server display
~~~~~~~~~~~~~~~~~~~~

Options to remove 'Named Server' functionality for users on their home page. 
You can remove the named server section and/or the new bottom section where servers started to act as dashboards are hidden.

Please note it will still be possible for users to create named servers if they know the direct API URLs.

::

    c.JupyterHub.template_vars = {
        'cds_hide_user_named_servers': False,
        'cds_hide_user_dashboard_servers': False
        }

Dashboard server name
~~~~~~~~~~~~~~~~~~~~~

To change the server name of your published dashboards:

::

    c.CDSDashboardsConfig.server_name_template = 'dash-{urlname}-{date}-{time}'

This template variable can use {urlname} (the URL-safe version of the dashboard name), {date} (current date in YYmmdd format),
and {time} (current date in HHMMSS format).

The default is 'dash-{urlname}'. The key advantage of the default (which does not use date/time) is that updated dashboards will replace old 
versions of the dashboard which keeping the URL the same. There is a higher risk of clashing with other servers (e.g. if the user decides to name 
one of their Jupyter servers similarly).

Using e.g. '{urlname}-{date}-{time}' will mean older dashboard servers 'expire' when replaced, which may be important to your use case. 
If using DockerSpawner, it is easier to match urlname-date-time against the commit of the docker image used to create the dashboard server.

Presentation Types
~~~~~~~~~~~~~~~~~~

By default, all supported presentation frameworks will be available for new dashboards. 
`Voilà <https://github.com/voila-dashboards/voila>`__ (for user-friendly display of Jupyter notebooks), 
`Streamlit <https://www.streamlit.io/>`__, and `Plotly Dash <https://plotly.com/dash/>`__ are the supported frameworks for dashboards.

To change the available set - for example, to remove streamlit and plotlydash as a possible selection for your users on the New Dashboard page, 
add the following to your jupyterhub_config.py:

::

    c.CDSDashboardsConfig.presentation_types = ['voila']

Or 

::

    c.CDSDashboardsConfig.presentation_types = ['streamlit', 'plotlydash']

to allow streamlit and plotlydash, but not voila.

The default is to allow all built-in types:

::

    c.CDSDashboardsConfig.presentation_types = ['voila', 'streamlit', 'plotlydash', 'bokeh', 'rshiny']

.. _default_allow_all:

Default User Access to Dashboards
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Control whether 'All Users' or 'Selected Users' is selected by default on the 'New Dashboard' page.

By default, 'All Users' will be selected.

To change this, in your jupyterhub_config.py file:

::

    c.CDSDashboardsConfig.default_allow_all = False

Now the 'New Dashboard' page will have 'Selected Users' highlighted by default. If the dashboard creator does not change this, and does not 
specify any user names in the list, then no-one apart from themselves will have access to the dashboard.


Voilà template
~~~~~~~~~~~~~~

To change the default template for Voilà presentations, add the following to your jupyterhub_config.py:

::

    c.VariableMixin.voila_template = 'default'

The template must already be installed in your user Python environment. 
Specify a blank string to instruct no template to be specified on the Voilà command line.

Server Timeouts and Keep Alive
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following settings are available in your jupyterhub_config.py to configure how the system responds to user activity in the dashboard servers:

::

    c.VariableMixin.proxy_force_alive = True
    c.VariableMixin.proxy_last_activity_interval = 300
    c.VariableMixin.proxy_request_timeout = 0

The default values are shown above.

proxy_last_activity_interval is the time interval in seconds before the dashboard server (actually, the jhsingle-native-proxy process) reports back to 
the hub whether activity has been seen on the dashboard server. The default of 300 will not be passed through to the process since it is the default value.

If proxy_force_alive is True (default) then the dashboard will report that there has been activity, even if there hasn't been. This is in order to keep the 
dashboard running so it is available for users in the future. Some JupyterHubs may cull idle servers after a certain amount of inactivity. This makes more 
sense for single user Jupyter servers where the user might expect to restart their own server, but is often not desirable for dashboards.

The proxy_request_timeout setting is an the timeout in seconds to allow the subprocess to startup. For large Voilà notebooks, this may need to be increased. 
The default value of 0 means that no value is passed as --request-timeout to jhsingle-native-proxy which then causes it to use its own default of 300. Note 
this default behavior is different to the proxy_last_activity_interval because a proxy_last_activity_interval value of 0 means something to jhsingle-native-proxy.

.. _docker_source_servers:

Source Servers
~~~~~~~~~~~~~~

The following options are currently only used by the DockerSpawner.

DockerSpawner users have extra functionality available whereby the dashboard creator 
can select a 'source server' to clone (*docker commit*). The dashboard server will be built out of that image, meaning any extra packages installed in the 
source server will be 
available. Likewise, if your home folder is built into the container rather than mounted as a volume, the source files will be copied into the new 
dashboard server.

Unless 
different servers are likely to have different files or packages installed, it probably won't make much difference which server is selected 
as the source anyway - most JupyterHubs will share the user's home file system across the different servers, so the Dashboard will 
be able to locate your notebooks and files. Most JupyterHubs maintain a central Docker image that contains all required packages, so users rarely 
install packages into their own server exclusively.

In your jupyterhub_config.py file:

::

    c.CDSDashboardsConfig.show_source_servers = True
    c.CDSDashboardsConfig.require_source_server = True

If show_source_servers is True, the create/edit Dashboard page will allow the dashboard creator to select a source server to clone. If require_source_server 
is False, there will also be a 'No Server' option to maintain the default behavior of starting a new dashboard server based on the usual Jupyter server 
configuration. If require_source_server is True, there will be no such option and a source server must be selected (your 'Default Server' will be available, 
along with any non-dashboard named servers).

File Source
~~~~~~~~~~~

If you don't want users to be able to enter a git repo as a source for dashboard files, add the following to your jupyterhub_config.py file:

::

    c.CDSDashboardsConfig.show_source_git = False

This will remove the git repo selection in the new/edit dashboard page, forcing all dashboards to be based on files from the Jupyter Tree.

The default value is true.


.. _conda_envs:

Conda Environments
~~~~~~~~~~~~~~~~~~

To allow users to select a Conda environment in which the dashboard should run, you can provide a list of Conda env names in your jupyterhub_config.py file:

::

    c.CDSDashboardsConfig.conda_envs = ['env1', 'env2', 'myenv', 'anotherenv']

This will add a dropdown to the new/edit dashboard page showing these selections in addition to a 'Default / None' option. The 'Default / None' option will 
be equivalent to the default behavior which runs the dashboard in whichever 'singleuser server' environment it finds (which may or may not be a Conda env 
at all). If a named Conda env is selected for the dashboard, the singleuser server (i.e. jhsingle-native-proxy) will actively attempt to switch to the 
named conda env.

For the conda env activation to work, :code:`conda` must be available on the path. Locating the named Conda env is done by iterating through the list of 
envs supplied e.g. by :code:`conda env list` and matching by the name of the right-most folder, returning whichever Conda env path it matches first.

It may be possible for env names to be duplicated, in which case only the first match can ever be activated.

If you have trouble making your Conda envs available to dashboards, please :ref:`get in touch<contact>` since more work may be required to cater for 
relatively common but non-standard Conda installations.

Note that Jupyter notebooks (ipynb files) may already contain the details of the Conda env in which they were created - since the different Conda 'kernels' 
are already available to Jupyter if registered using ipykernel. Therefore, Voilà may already be capable of switching to the desired Conda env (kernel) 
when it runs the notebook, and thus you may not need to specify Conda envs through :code:`c.CDSDashboardsConfig.conda_envs` at all in order for everything 
to work if Voilà is the only relevant dashboard framework type.

See also :ref:`conda_kernels_voila`.

Presentation Cmd
~~~~~~~~~~~~~~~~

The command run to start a dashboard server can be changed by setting :code:`c.VariableMixin.default_presentation_cmd` (similar to changing Spawner.cmd, but 
only affecting dashboard servers). It can also be overridden to affect each presentation type (e.g. streamlit only).

See :ref:`custom launchers <customlaunchers>` and :ref:`default_presentation_cmd`.

Mailing List for Updates
~~~~~~~~~~~~~~~~~~~~~~~~

Please `sign up to the ContainDS email list <https://containds.com/signup/>`__ to receive notifications about updates to the project including new 
features and security advice.

.. _changelog:


Changelog
---------

Version 0.5.5
~~~~~~~~~~~~~

Released 20 Apr 2021

- Added proxy_ready_timeout and proxy_websocket_max_message_size options to c.VariableMixin (these are 
  config options passed to jhsingle-native-proxy).


Version 0.5.3
~~~~~~~~~~~~~

Released 13 Apr 2021

- Fix relative dashboards-static URLs for assets which weren't found in some JupyterHub configurations
- Also fix a dashboard redirect for the same reason (some JupyterHubs not redirecting as expected)
- Depend on jhsingle-native-proxy >= 0.7.3
- Use --progressive flag of jhsingle-native-proxy for Voila launchers, so the 'loading' page appears sooner


Version 0.5.1
~~~~~~~~~~~~~

Released 8 Apr 2021

- Fixed a 500 error when accessing /home-cds (:ref:`restricted mode <restrictusers>`) when not logged in
- VariableSudoSpawner contributed by `StevenLaan <https://github.com/StevenLaan>`__.

Version 0.5.0
~~~~~~~~~~~~~

Released 23 Mar 2021

- Dashboard servers are started using default spawner options by default, but a new spawn_default_options 
  config option can be set to False to require the dashboard owner to select spawner options (if any) when first started. 
  See :ref:`spawn_default_options`.
- Breaking change: if you specify conda_envs options for your dashboard creators to choose a Conda environment for their users 
  there was always a 'Default / None' option added at the top of the list, corresponding to 'no Conda env'. You now have to 
  specify an empty string explicitly in conda_envs if you want a 'Default / None' option to appear. See :ref:`conda_envs`.

Version 0.4.3
~~~~~~~~~~~~~

Released 6 Jan 2021

- Corresponds to `jhsingle-native-proxy 0.6.1 <https://github.com/ideonate/jhsingle-native-proxy>`__ with Python 3.9 compatibility

Version 0.4.2
~~~~~~~~~~~~~

Released 16 Dec 2020

- Compatibility with JupyterHub 1.3
- Options to return info about auth_state and servers from the experimental :ref:`userinfoapi`

Version 0.4.1
~~~~~~~~~~~~~

Released 20 Nov 2020

- Git branch can now be specified when creating a dashboard (thanks to contribution from `slemonide <https://github.com/slemonide>`__)
- Corresponds to `jhsingle-native-proxy 0.6.0 <https://github.com/ideonate/jhsingle-native-proxy>`__ with better handling of logs from subprocess

Version 0.4.0
~~~~~~~~~~~~~

Released 11 Nov 2020

- Functionality to split users into non-technical or developers groups.
- UI alternatives for /hub/home-cds to prevent non-technical users being presented with 'My Server' or dashboard buttons.
- Group management UI in admin pages.
- See :ref:`restrictusers` for more details.
- Merge trait dicts (e.g. Env vars) in Spawners, fix of `issue 43 <https://github.com/ideonate/cdsdashboards/issues/43>`__.

Version 0.3.5
~~~~~~~~~~~~~

Released 18 Sep 2020

- Stricter checks that dashboard start_path is not absolute.
- Fix to allow Streamlit components to work in iframes (requires config - see :ref:`streamlit_components`).
- Corresponds to jhsingle_native_proxy release 0.5.6 (always passes an absolute presentation_path to subcommand).

Version 0.3.4
~~~~~~~~~~~~~

Released 3 Sep 2020

- Automatically redirect to dashboard when ready (no 'Go to Dashboard' button anymore).
- allow_custom_conda_env config option means dashboard creator can type their own conda env name or path.
- More chars (' and ") allowed in start path file names.
- Added /hub/dashboards-api/hub-info/user endpoint to aid getting current user info in dashboards.
- Includes jhsingle-native-proxy 0.5.4, changes current working folder to the git root if dashboard created from a git repo source.

Version 0.3.3
~~~~~~~~~~~~~

Released 31 Aug 2020

- Allows use of the companion `JupyterLab extension <https://www.npmjs.com/package/@ideonate/jupyter-containds>`__ to publish and edit dashboards directly from a 
  JupyterLab session inside a regular singleuser Jupyter server running in JupyterHub.

Version 0.3.2
~~~~~~~~~~~~~

Released 17 Aug 2020

- Streamlit fix where xrsf protection was preventing file uploads. Now pass origin (browser.serverAddress) to streamlit command, requires jhsingle-native-proxy>=0.5.0.
- Added default_presentation_cmd to VariableMixin which is set to ['start.sh', 'python3', '-m', 'jhsingle_native_proxy.main'] for DockerSpawner/KubeSpawner
  setups, and remains as ['python3', '-m', 'jhsingle_native_proxy.main'] for process spawners. The start.sh script sources files in /usr/local/bin/before-notebook.d
  which is useful for e.g. incorporating GitHub tokens into the environment. This requires the singleuser image to contain the start.sh script of course (those 
  based on docker-stacks should do already).

Version 0.3.0
~~~~~~~~~~~~~

Released 23 July 2020

- User permissions: choose 'All Users' or 'Selected Users' for each dashboard to restrict access.
- Conda Envs: select from a list of available Conda envs in which your dashboard should run - see :ref:`conda_envs`.


Version 0.2.0
~~~~~~~~~~~~~

Released 16 July 2020

- Git Repos can be used as a source for files (otherwise, pull from Jupyter Tree as before).
- Installation of components is now available via conda-forge (thanks to `Frédéric Collonval <https://github.com/fcollonval>`__).

Version 0.1.0
~~~~~~~~~~~~~

Released 8 July 2020

- DockerSpawner major changes: requires use of an enhanced spawner. Set jupyterhub_config.py as follows:
  :code:`c.JupyterHub.spawner_class = 'cdsdashboards.hubextension.spawners.variabledocker.VariableDockerSpawner'`
  This is to bring DockerSpawner into line with the other spawners. See `GitHub Issue <https://github.com/ideonate/cdsdashboards/issues/13>`__ for rationale.
- By default, there is no longer a 'source server' selection on the create/edit dashboard page. This is because it has no effect for most spawners 
  and now is not expected by VariableDockerSpawner. It can be enabled as described in :ref:`docker_source_servers`, allowing users to clone 
  (*docker commit*) an existing server as a Docker image to be used for the new dashboard server.

Version 0.0.20
~~~~~~~~~~~~~~

Released 30 June 2020

Remember to upgrade both hub and user environments:

Hub command:

::

    python3 -m pip install --upgrade cdsdashboards==0.0.20

User command:

::

    python3 -m pip install --upgrade cdsdashboards[user]==0.0.20

- Installation dependencies simplified (docker dependency no longer installed - we now assume you have docker if you are already using DockerSpawner)
- pip install cdsdashboards[user] installs the basic (low-dependency) wrapper scripts needed in your user environment. You also need to install voila, streamlit etc yourself.
- Bokeh server fix for slow starting processes, should now be more reliable. (Requires bokeh-root-cmd >= 0.0.5)
- Defaults to keeping dashboard servers alive by reporting activity (even where none is detected). This is to avoid cull idle server processes from stopping dashboards. 
  Requires jhsingle-native-proxy >= 0.3.2. This behavior can be configured, see :ref:`useroptions_timeouts`.
- More robust handling of edge cases when building dashboard (e.g. if source server happens to be terminating)

Version 0.0.19
~~~~~~~~~~~~~~

Released 18 June 2020

- Support for R Shiny Server and custom frameworks (presentation types)

Version 0.0.18
~~~~~~~~~~~~~~

Released 11 June 2020

- Support for Bokeh (and Panel) frameworks

Version 0.0.17
~~~~~~~~~~~~~~

Released 9 June 2020

- Preliminary support for Kubernetes-based JupyterHubs (Zero to JupyterHub)

Version 0.0.16
~~~~~~~~~~~~~~

Released 5 June 2020

- Help text on Dashboard Edit page, explaining relative path is required. Help button links to project docs.
- Problems with underlying frameworks (e.g. Voilà, Dash) are now displayed with detailed error messages in place of the Dashboard.

Please remember to upgrade your hub environment (cdsdashboards package) and also your user environment (cdsdashboards or just jhsingle-native-proxy package).

Version 0.0.15
~~~~~~~~~~~~~~

Released 2 June 2020

- Improvements to the Database Upgrade process when migrating to newer versions of cdsdashboards.

Version 0.0.14
~~~~~~~~~~~~~~

Released 2 June 2020

- Plotly Dash added as a framework option. If not visible, remove or update presentation_types configuration option (default: :code:`c.CDSDashboardsConfig.presentation_types = ['voila', 'streamlit', 'plotlydash']`)

Version 0.0.13
~~~~~~~~~~~~~~

Released 1 June 2020

- Streamlit added as a framework option, in addition to Voilà.
- server_name_template configuration option added to change the URL of Dashboard servers (default :code:`c.CDSDashboardsConfig.server_name_template = 'dash-{urlname}-{date}-{time}'`).
- presentation_types configuration option added (default: :code:`c.CDSDashboardsConfig.presentation_types = ['voila', 'streamlit']`)

If upgrading from version 0.0.11, the database will require an update. ContainDS Dashboards will prompt for this to happen within the JupyterHub website. 

Upgrade the package: :code:`python -m pip install --upgrade cdsdashboards==0.0.13`

You must upgrade the user environment as well as the hub environment. (This may not be applicable if you are using DockerSpawner, but instead you may need to 
:code:`docker pull` the latest image, or otherwise upgrade it (e.g. use ideonate/containds-all-scipy) if you wish to make Streamlit dashboards.)

Restart JupyterHub. You may see 500 errors on the Home page. Go to the Dashboards menu where you should see a prompt to upgrade the database, including 
an 'Upgrade Database' button if you are an admin.

Please backup the database first - sqlite databases will be backed up automatically with a timestamped file in the same folder as the original.

Any problems with the upgrade, please :ref:`get in touch<contact>`. 


Version 0.0.11
~~~~~~~~~~~~~~

Released 26 May 2020

- VariableSystemdSpawner (and VariableUserCreatingSpawner) allows {DASHSERVERNAME} in the unit_name_template configuration, so it can work with named servers.


Version 0.0.9
~~~~~~~~~~~~~

Released 25 May 2020

- VariableUserCreatingSpawner for use in place of the default spawner in TLJH.


Version 0.0.8
~~~~~~~~~~~~~

Released 25 May 2020

- LocalProcessSpawner and SystemdSpawner are now supported
- Can specify start URL path of the dashboard
- c.CDSDashboardsConfig.builder_class must now always be specified in jupyterhub_config.py
- No longer requires tornado_extra_settings in jupyterhub_config.py
- Now uses c.JupyterHub.template_paths = CDS_TEMPLATE_PATHS (instead of [CDS_TEMPLATE_PATH] previously)


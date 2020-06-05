.. _changelog:


Changelog
---------

Version 0.0.16
~~~~~~~~~~~~~~

Released 5 June 2020

- Help text on Dashboard Edit page, explaining relative path is required. Help button links to project docs.
- Problems with underlying frameworks (e.g. Voila, Dash) are now displayed with detailed error messages in place of the Dashboard.

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

- Streamlit added as a framework option, in addition to Voila.
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


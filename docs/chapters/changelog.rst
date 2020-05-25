.. _changelog:


Changelog
---------

Version 0.0.8
~~~~~~~~~~~~~

Released 25 May 2020

- LocalProcessSpawner and SystemdSpawner are now supported
- Can specify start URL path of the dashboard
- c.CDSDashboardsConfig.builder_class must now always be specified in jupyterhub_config.py
- No longer requires tornado_extra_settings in jupyterhub_config.py
- Now uses c.JupyterHub.template_paths = CDS_TEMPLATE_PATHS (instead of [CDS_TEMPLATE_PATH] previously)





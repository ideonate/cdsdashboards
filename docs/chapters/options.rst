.. _options:


Options
~~~~~~~

There are extra options that can be added to your jupyterhub_config.py file.

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

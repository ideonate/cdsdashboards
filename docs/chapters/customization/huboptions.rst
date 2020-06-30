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
`Voila <https://github.com/voila-dashboards/voila>`__ (for user-friendly display of Jupyter notebooks), 
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

Voila template
~~~~~~~~~~~~~~

To change the default template for Voila presentations, add the following to your jupyterhub_config.py:

::

    c.VariableMixin.voila_template = 'default'

The template must already be installed in your user Python environment. 
Specify a blank string to instruct no template to be specified on the Voila command line.

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

The proxy_request_timeout setting is an the timeout in seconds to allow the subprocess to startup. For large Voila notebooks, this may need to be increased. 
The default value of 0 means that no value is passed as --request-timeout to jhsingle-native-proxy which then causes it to use its own default of 300. Note 
this default behavior is different to the proxy_last_activity_interval because a proxy_last_activity_interval value of 0 means something to jhsingle-native-proxy.


Mailing List for Updates
~~~~~~~~~~~~~~~~~~~~~~~~

Please `sign up to the ContainDS email list <https://containds.com/signup/>`__ to receive notifications about updates to the project including new 
features and security advice.

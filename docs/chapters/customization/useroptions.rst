.. _useroptions:


User Server Options
-------------------

There are extra options that can be added to your jupyterhub_config.py file. 
(See `here <http://tljh.jupyter.org/en/latest/topic/escape-hatch.html>`__ for how to add config on The Littlest JupyterHub.)


.. _useroptions_timeouts:


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


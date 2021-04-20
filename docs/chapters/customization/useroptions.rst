.. _useroptions:


User Server Options
-------------------

There are extra options that can be added to your jupyterhub_config.py file. 
(See `here <http://tljh.jupyter.org/en/latest/topic/escape-hatch.html>`__ for how to add config on The Littlest JupyterHub.)


Presentation Cmd
~~~~~~~~~~~~~~~~

The command run to start a dashboard server can be changed by setting :code:`c.VariableMixin.default_presentation_cmd` (similar to changing Spawner.cmd, but 
only affecting dashboard servers). It can also be overridden to affect each presentation type (e.g. streamlit only).

See :ref:`custom launchers <customlaunchers>` and :ref:`default_presentation_cmd`.

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

The proxy_request_timeout setting is the timeout in seconds to allow the subprocess to respond to each http request. 
For large Voilà notebooks, this may need to be increased. 
The default value of 0 means that no value is passed as --request-timeout to jhsingle-native-proxy which then causes it to use its own default of 300. Note 
this default behavior is different to the proxy_last_activity_interval because a proxy_last_activity_interval value of 0 means something to jhsingle-native-proxy.

Other timeout and size settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

proxy_ready_timeout
===================

::

    c.VariableMixin.proxy_ready_timeout = 30


Ready timeout in seconds that jhsingle-native-proxy should allow the underlying process to wait during startup before failing if still
unable to respond at the --ready-check-path URL.

The default of 0 means that no --ready-timeout flag will be passed to jhsingle-native-proxy so it will use its own default.

proxy_websocket_max_message_size
================================

::

    c.VariableMixin.proxy_websocket_max_message_size = 10*1024*1024


Max websocket message size allowed by jhsingle-native-proxy, passed as --websocket-max-message-size on the command line.
The default of 0 means that no --websocket-max-message-size flag will be passed to jhsingle-native-proxy so it will use its own 
default (the same value as shown above, at the time of writing).


Voilà template
~~~~~~~~~~~~~~

To change the default template for Voilà presentations, add the following to your jupyterhub_config.py:

::

    c.VariableMixin.voila_template = 'default'

The template must already be installed in your user Python environment. 
Specify a blank string to instruct no template to be specified on the Voilà command line.


JupyterLab Extension
--------------------

There is a companion JupyterLab extension allowing one-click set up of Voila dashboards based on the current ipynb notebook in a regular Jupyter 
server. It also provides direct links to edit existing dashboards. See 
`JupyterLab ContainDS extension <https://www.npmjs.com/package/@ideonate/jupyter-containds>`__.

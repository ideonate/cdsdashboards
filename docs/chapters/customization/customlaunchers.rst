.. _customlaunchers:


Custom Launchers
----------------

It is possible to add your own presentation types (i.e. frameworks, like the built-in Streamlit or Voilà) by specifying the details of 
a new launcher.  You can also modify the built-in types to suit your environment if necessary.

This is an advanced topic for which programming experience would be beneficial.

Enabling your own Launcher
~~~~~~~~~~~~~~~~~~~~~~~~~~

Adding a new presentation type so that it is available in the Framework dropdown on the New/Edit Dashboard page is easy. Linking it up 
so that it launches correctly can be slightly more complicated.

To add it to the list, edit your jupyterhub_config.py file or similar. For example, to add 'custom-panel' for an alternative way to 
invoke your own format of Panel scripts, specify:

::

    c.CDSDashboardsConfig.extra_presentation_types = ['custom-panel']

This will add it to the list of built-in types. You can also just add it to your own presentation_types:

::

    c.CDSDashboardsConfig.presentation_types = ['voila', 'streamlit', 'plotlydash', 'custom-panel']

The complete list is just the sum of presentation_types and extra_presentation_types - the reason for having two separate lists is so 
you can add your own types to extra_presentation_types without clobbering the default built-in list.

After restarting JupyterHub, the custom presentation type should be available in the dropdown on the New Dashboard page - but it will not 
successfully launch a dashboard until you have also configured a launcher.


Configuring your Launcher
~~~~~~~~~~~~~~~~~~~~~~~~~

An extra_presentation_launchers configuration dict must be added to your jupyterhub_config.py

::

    import os
    dirname = os.path.dirname(__file__)

    c.VariableMixin.extra_presentation_launchers = {
        'custom-panel': {
            'args': [
                'python3', '{presentation_basename}', '{port}', '{origin_host}'
                ],
            'debug_args': [],
            'env': {
                'PYTHONPATH': os.path.join(dirname, '/home/{username}/{presentation_dirname}')
            }
        }
    }

    c.CDSDashboardsConfig.extra_presentation_types = ['custom-panel']


Note you can add the config under c.VariableKubeSpawner (or whichever spawner you are using) instead of c.VariableMixin (a superclass) if 
that makes it clearer. For this documentation, it is easier to use c.VariableMixin so it will work verbatim for all relevant spawners.

The above is an attempt to run a Python script directly into the python interpreter. The substitution variable {presentation_path} will 
be the full path of the Python file as provided by the user who is creating the dashboard. Their script should expect a port number and 
a web origin as the two 'argv' parameters.

The user probably runs the script on their own command line as :code:`python3 /home/dan/myscripts/script_name.py`, except subsituting the full path to the py 
file themselves.

Within ContainDS Dashboards you can see that PYTHONPATH has to be set to work correctly. The variables {presentation_basename} and 
{presentation_path} are derived from {presentation_path} using os.path.basename and os.path.dirname Python functions. So in the context 
of JupyterHub, the script is actually run as :code:`python3 script_name.py 85124 myjupyterhub.net`. And 
PYTHONPATH is set to /home/dan/myscripts (assuming the location is still the same once uploaded to the Jupyter server).

Example Custom Python Script, showing how the parameters passed allow the script to run on an arbitrary port:

::

    port = 80
    websocket_origin = None
    show = True
    index_html=None

    # We need to alter these things to run behind a reverse proxy
    import sys, os
    if len(sys.argv) >= 3:
        port = int(sys.argv[1])
        websocket_origin = sys.argv[2]
        show = False

        # The root index html in Panel isn't quite right for this case - will submit an issue
        # Here, we modify to use our own version. Obviously, it's not efficient to do this on every run, 
        # but this is a clear way to see what needs to be different!    
        from panel.io.server import INDEX_HTML
        index_html = os.path.join(os.path.dirname(os.path.abspath(__file__)), "panelindex.html")
        with open(index_html, 'w') as outfile:
            with open(INDEX_HTML, 'r') as infile:
                for s in infile.readlines():
                    outfile.write(s.replace('{{ prefix }}', '.'))


    import panel as pn

    def app1():
        return pn.pane.Markdown("# Hello From app1")

    def app2():
        return pn.pane.Markdown("# Hello From app2")

    ROUTES = {
        "panel-app1": app1, "panel-app2": app2
    }

    pn.config.sizing_mode="stretch_width"

    opts = {
        'port': port,
        'title': "Example",
        'websocket_origin': websocket_origin,
        'show': show
    }

    if index_html:
        opts['index'] = index_html

    pn.serve(ROUTES, **opts)



For a deeper understanding, see the built-in launchers in 
the `cdsdashboards code <https://github.com/ideonate/cdsdashboards/blob/master/cdsdashboards/hubextension/spawners/variablemixin.py>`__.

It is also possible to modify the built-in launchers by specifying just the entries you want to change in the extra_presentation_launchers 
configuration. For example:

::

    c.VariableMixin.extra_presentation_launchers = {
        'bokeh': {
            'env': {
                'MY_ENV_VAR': 'SOMEVALUE')
            }
        }
    }


The whole custom launchers feature is experimental, and you are encouraged to :ref:`contact <contact>` the authors to discuss any requirements. 

.. _default_presentation_cmd:

cmd and args
============

The cmd that is run to start the launcher is set by :code:`c.VariableMixin.default_presentation_cmd` (a list). This can be overridden in your 
jupyterhub_config, or on a per-launcher basis by setting a 'cmd' key/value in your launcher dict.

The default value of default_presentation_cmd is set to :code:`['start.sh', 'python3', '-m', 'jhsingle_native_proxy.main']` for 
DockerSpawner/KubeSpawner setups, and is :code:`['python3', '-m', 'jhsingle_native_proxy.main']` for process spawners. 

args can be overriden per-launcher only.

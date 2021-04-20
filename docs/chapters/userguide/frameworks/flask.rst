.. _flask:

Flask Apps
----------

Flask support is currently experimental.

Please ask your admin to make the following changes to jupyterhub_config:

::

   c.CDSDashboardsConfig.extra_presentation_types = ['flask']

   c.VariableMixin.extra_presentation_launchers = {
      'flask': {
         'args': ['--destport=0', 'python3', '{-}m','flask_gunicorn_cmd.main', '{presentation_path}',
               '{--}port={port}']
      },
   }

You will also need to install the `flask-gunicorn-cmd <https://github.com/ideonate/flask-gunicorn-cmd>`__ 
Python package in your JupyterHub user image or environment.

This should provide an extra 'flask' presentation framework option when you create a dashboard.

Provide the path to your Flask Python file.

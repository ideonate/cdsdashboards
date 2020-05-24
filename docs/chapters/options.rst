.. _options:


Options
~~~~~~~

There are extra options that can be added to your jupyterhub_config.py file.

Options to remove 'Named Server' functionality for users on their home page. 
You can remove the named server section and/or the new bottom section where servers started to act as dashboards are hidden.

Please note it will still be possible for users to create named servers if they know the direct API URLs.

::

    c.JupyterHub.template_vars = {
        'cds_hide_user_named_servers': False,
        'cds_hide_user_dashboard_servers': False
        }


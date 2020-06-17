.. _finetune:


Fine Tune the User Experience
=============================

Now that non-technical users may be logging in to your JupyterHub, you may want to simplify the login process for them.

In particular, they don't want to be encouraged to start their own Jupyter server if they are only really logging in to view dashboards 
created by others.

The following jupyterhub_config.py snippet will make the default behavior to start off on the Dashboards list page, and not to automatically 
redirect to their 'My Server' when they hit the home page:

::

    c.JupyterHub.redirect_to_server = False
    c.JupyterHub.default_url = '/hub/dashboards'


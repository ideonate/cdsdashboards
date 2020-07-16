.. _bokehpanel:

Bokeh or Panel apps
-------------------

How to turn your `Bokeh <https://docs.bokeh.org/>`__ or `Panel <https://panel.holoviz.org/>`__ app or notebook into a Dashboard.

Preparing your Code
~~~~~~~~~~~~~~~~~~~

You can use 'My Server' (or a named server) to upload any notebooks, or Python files and data, that form your app or notebook.

In our example, we will take a Panel app straight from a GitHub repo. We have a Panel app in a Jupyter notebook called 
Panel_Introduction.ipynb, available on 
`GitHub here <https://github.com/ideonate/cdsdashboards/tree/master/examples/sample-source-code/panel>`__.

New Dashboard
~~~~~~~~~~~~~

Click 'Dashboards' in the menu bar. Then click 'New Dashboard'.

.. figure:: ../../../_static/screenshots/userguide/frameworks/PanelNewDashboard.png
   :alt: New Dashboard screen

Fill in a name and optionally a description.

Click 'Git Repo' and enter the URL: :code:`https://github.com/ideonate/cdsdashboards`

Select the framework required. For our example, we need to change this to *bokeh*.

Specify the URL-path to our Bokeh/Panel app, relative to the Jupyter server's home folder. This can be a Python py file, an ipynb notebook, or a 
folder containing at least a main.py file.

In our case, Panel_Introduction.ipynb is the file we need, but it is a few folders deep in the Git repo, so we enter:

:code:`examples/sample-source-code/panel/Panel_Introduction.ipynb`

**Note that your Dashboard will be accessible by any other JupyterHub user.**

Click 'Save'.

Building the Dashboard
~~~~~~~~~~~~~~~~~~~~~~

When you click Save, the dashboard will be built automatically. This just means that a new named server is created based on your new Dashboard, 
but running the Bokeh server instead of Jupyter.

Once the Dashboard is built, click the 'Go to Dashboard' button to open the dashboard in a new tab.

The Bokeh/Panel app is displayed:

.. figure:: ../../../_static/screenshots/userguide/frameworks/PanelApp.png
   :alt: Dashboard screen

See :ref:`working with dashboards<working>` to understand more about how Dashboards operate, including sharing them with colleagues.

Panel and Voila
~~~~~~~~~~~~~~~

Note that for Panel apps built in ipynb notebooks, it is also possible to select the 'voila' framework to deploy them as dashboards. Voila 
is more closely related to the Jupyter notebook server, whereas selecting 'bokeh' as the framework uses the equivalent of the 'dash serve' command. 
It will most often make sense to select 'bokeh', but it is worth being aware that 'voila' is a possible backup for Panel notebooks.

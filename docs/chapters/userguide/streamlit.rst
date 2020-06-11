.. _streamlit:

Streamlit Apps
--------------

How to turn your `Streamlit <https://streamlit.io/>`__ app into a Dashboard.

Preparing your Code
~~~~~~~~~~~~~~~~~~~

Use 'My Server' (or a named server) to upload any Python files and data that form your Streamlit app.

Below, we have a Streamlit app in a Python file called intro.py. To try out this example, you can obtain the 
`source code here <https://github.com/ideonate/cdsdashboards/tree/master/examples/sample-source-code/streamlit>`__.

.. figure:: ../../_static/screenshots/userguide/JupyterTree.png
   :alt: Jupyter with ipynb and py files

Streamlit apps can't normally be run at this stage (in Jupyter), so for now you would upload Python files and data that you have developed on 
your own machine.

Click 'Control Panel' to go back to JupyterHub.


New Dashboard
~~~~~~~~~~~~~

Click 'Dashboards' in the menu bar. You will see the page showing any Dashboards created by you, or shared with you by colleagues.

Below, we have already created a separate :ref:`Voila<voila>` Dashboard, but in this section we can ignore that and focus on making our 
Streamlit dashboard:

.. figure:: ../../_static/screenshots/userguide/VoilaDashboardOnly.png
   :alt: Dashboards screen showing a Voila dashboard

Click 'New Dashboard'.

.. figure:: ../../_static/screenshots/userguide/StreamlitNewDashboard.png
   :alt: New Dashboard screen

Fill in a name and optionally a description.

The default My Server should already be selected as the source. If you have other named servers they should be available here. Unless 
different servers are likely to have different files or packages installed, it probably won't make much difference which server is selected 
as the source anyway - most JupyterHubs will share the user's home file system across the different servers, so the Dashboard will 
be able to locate your notebooks and files.

Select the framework required. For our example, we need to change this to *streamlit*.

Specify the URL-path to the Python file of our Streamlit app, relative to the Jupyter server's home folder. In our case, intro.py 
was at the top level in our Jupyter tree, so we just enter intro.py.

**Note that your Dashboard will be accessible by any other JupyterHub user.**

Click 'Save'.

Building the Dashboard
~~~~~~~~~~~~~~~~~~~~~~

When you click Save, the dashboard will be built automatically. This just means that a new named server is created based on your new Dashboard, 
running Streamlit instead of the regular Jupyter server.

This is what you should see while the build is taking place:

.. figure:: ../../_static/screenshots/userguide/StreamlitDashboardBuild.png
   :alt: Dashboard Build screen

Any errors during the build will be visible here.

Once the Dashboard is built, click the 'Go to Dashboard' button to open the dashboard in a new tab.

The Streamlit app is displayed:

.. figure:: ../../_static/screenshots/userguide/StreamlitApp.png
   :alt: Dashboard screen

See :ref:`working with dashboards<working>` to understand more about how Dashboards operate, including sharing them with colleagues.

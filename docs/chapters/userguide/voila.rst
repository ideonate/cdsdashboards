.. _voila:

Jupyter (Voila) Dashboards
--------------------------

How to build a Jupyter notebook-based Dashboard.

Preparing your Code
~~~~~~~~~~~~~~~~~~~

Use 'My Server' (or a named server) to create a Jupyter notebook (ipynb file) as normal.

Below, we have an ipynb (Jupyter notebook) called Presentation.ipynb. To try out this example, you can obtain the 
`source code here <https://github.com/ideonate/cdsdashboards/tree/master/examples/sample-source-code/voila>`__. 
For this notebook to work you may need matplotlib, numpy, and ipywidgets to be installed in your user Python env.

.. figure:: ../../_static/screenshots/userguide/JupyterTree.png
   :alt: Jupyter with ipynb and py files

For Jupyter notebooks, of course you can run them as usual in your Jupyter server - and there is a 'Voila Preview' button so you can see how 
the final dashboard will appear. Voila is the name of the technology that is essentially a user-friendly and secure version of Jupyter notebooks: 
code cells are hidden, and the user can only view the intended end result. They can interact with widgets if they are present in the notebook though.

Click 'Control Panel' to go back to JupyterHub.


New Dashboard
~~~~~~~~~~~~~

Click 'Dashboards' in the menu bar. You will see the page showing any Dashboards created by you, or shared with you by colleagues.

Below, in a fresh installation of ContainDS Dashboards, there are no Dashboards:

.. figure:: ../../_static/screenshots/userguide/EmptyDashboards.png
   :alt: Empty Dashboards screen

Click 'New Dashboard'.

.. figure:: ../../_static/screenshots/userguide/NewDashboard.png
   :alt: New Dashboard screen

Fill in a name and optionally a description.

The default My Server should already be selected as the source. If you have other named servers they should be available here. Unless 
different servers are likely to have different files or packages installed, it probably won't make much difference which server is selected 
as the source anyway - most JupyterHubs will share the user's home file system across the different servers, so the Dashboard will 
be able to locate your notebooks and files.

Select the framework required. For our Jupyter notebook (ipynb) file, we need to leave this as 'voila'.

Specify the URL-path to the ipynb file, relative to the Jupyter server's home folder. In our case, Presentation.ipynb was at the top level in our 
Jupyter tree, so we just enter Presentation.ipynb. It is important to get this right as file-not-found error messages are not currently propagated 
back up to JupyterHub easily. If in doubt, leave blank and Voila will just show the entire tree to the Dashboard user so they can locate the 
file themselves.

**Note that your Dashboard will be accessible by any other JupyterHub user.**

Click 'Save'.

Building the Dashboard
~~~~~~~~~~~~~~~~~~~~~~

When you click Save, the dashboard will be built automatically. This just means that a new named server is created based on your new Dashboard, 
running Voila instead of the regular Jupyter server.

This is what you should see while the build is taking place:

.. figure:: ../../_static/screenshots/userguide/DashboardBuild.png
   :alt: Dashboard Build screen

Any errors during the build will be visible here.

Once the Dashboard is built, click the 'Go to Dashboard' button to open the dashboard in a new tab.

The user-friendly and safe version of the notebook is displayed:

.. figure:: ../../_static/screenshots/userguide/DashboardView.png
   :alt: Dashboard screen

See :ref:`working with dashboards<working>` to understand more about how Dashboards operate, including sharing them with colleagues.

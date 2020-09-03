.. _voila:

Jupyter (Voilà) Dashboards
--------------------------

How to build a Jupyter notebook-based Dashboard, from your 'My Server' Jupyter tree.

Preparing your Code
~~~~~~~~~~~~~~~~~~~

Use 'My Server' (or a named server) to create a Jupyter notebook (ipynb file) as normal.

Below, we have an ipynb (Jupyter notebook) called Presentation.ipynb. To try out this example, you can obtain the 
`source code here <https://github.com/ideonate/cdsdashboards/tree/master/examples/sample-source-code/voila>`__. 
For this notebook to work you may need matplotlib, numpy, and ipywidgets to be installed in your user Python env.

.. figure:: ../../../_static/screenshots/userguide/frameworks/JupyterTree.png
   :alt: Jupyter with ipynb and py files

You can run the Jupyter notebook as usual in your Jupyter server - and there is a 'Voilà Preview' button so you can see how 
the final dashboard will appear. Voilà is the name of the technology that is essentially a user-friendly and secure version of Jupyter notebooks: 
code cells are hidden, and the user can only view the intended end result. They can interact with widgets if they are present in the notebook though.

Click 'Control Panel' to go back to JupyterHub.

New Dashboard
~~~~~~~~~~~~~

From the Dashboards page in JupyterHub, click 'New Dashboard'.

.. figure:: ../../../_static/screenshots/userguide/frameworks/FileSourceJupyterTree.png
   :alt: New Dashboard screen

Fill in a name and optionally a description.

Select the framework required. For our Jupyter notebook (ipynb) file, we need to leave this as 'voila'.

Specify the URL-path to the ipynb file, relative to the Jupyter server's home folder. In our case, Presentation.ipynb was at the top level in our 
Jupyter tree, so we just enter Presentation.ipynb. If in doubt, leave blank and Voilà will just show the entire tree to the Dashboard user so 
they can locate the file themselves.

**Note that your Dashboard will be accessible by any other JupyterHub user.**

Click 'Save'.

Once the Dashboard is built you will be automatically redirected to it.

The user-friendly and safe version of the notebook is displayed:

.. figure:: ../../../_static/screenshots/userguide/frameworks/DashboardView.png
   :alt: Dashboard screen

See :ref:`working with dashboards<working>` to understand more about how Dashboards operate, including sharing them with colleagues.

JupyterLab Extension
~~~~~~~~~~~~~~~~~~~~

There is a companion JupyterLab extension allowing one-click set up of Voila dashboards based on the current ipynb notebook in a regular Jupyter 
server. It also provides direct links to edit existing dashboards. See 
`JupyterLab ContainDS extension <https://www.npmjs.com/package/@ideonate/jupyter-containds>`__.

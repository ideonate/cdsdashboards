
ContainDS Dashboards
====================

A Dashboard publishing solution for Data Science teams to share results with decision makers.

Run a private on-premise or cloud-based JupyterHub with extensions to instantly publish Jupyter notebooks, Streamlit apps, or Plotly Dash apps as 
user-friendly interactive dashboards to share with non-technical colleagues.

JupyterHub is a way to run one website that provides Jupyter notebook environments to multiple users - your entire data science team, for example. 
To use ContainDS Dashboards, you will need a JupyterHub setup, but you don't need to use it as the main data science environment for your organisation. 
ContainDS Dashboards leverages the standardised security and authentication functionality of JupyterHub, which makes ContainDS Dashboards incredibly 
powerful, even if you don't believe your organisation requires a JupyterHub for any other purposes.

The cdsdashboards open source package allows users to create interactive Jupyter notebooks that can be instantly and reliably published as 
secure interactive `Voila <https://voila.readthedocs.io/en/stable/>`__ web apps. Any authorised JupyterHub user can view the dashboard.

Read a full description in :ref:`overview`.

Installation and Setup
~~~~~~~~~~~~~~~~~~~~~~

Once you have `set up JupyterHub <https://jupyterhub.readthedocs.io/en/stable/installation-guide.html>`__ on a server, you install the 
cdsdashboards package and make some simple configuration changes to jupyterhub_config.py.

ContainDS Dashboards currently works on single-server JupyterHubs (not currently Kubernetes-based). See :ref:`other requirements<requirements>`.

To continue installation please see :ref:`setup`

Mailing List
~~~~~~~~~~~~

Please `sign up to our email list <https://containds.com/signup/>`__ to receive notifications about updates and related news.

Documentation Contents
~~~~~~~~~~~~~~~~~~~~~~

.. toctree::
   :maxdepth: 3

   chapters/overview
   chapters/setup/setup
   chapters/userguide/userguide
   chapters/troubleshooting
   chapters/requirements
   chapters/changelog
   chapters/contact
   chapters/license


ContainDS Dashboards source code can be found on `GitHub here <https://github.com/ideonate/cdsdashboards>`_.


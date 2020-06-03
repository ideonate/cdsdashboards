.. _overview:

Overview
--------

`ContainDS <https://containds.com/>`__ is a data science platform for teams working on discrete projects. 
It provides simple infrastructure to share prototypes and dashboards based on any open source frameworks.

Your data scientists will always use their preferred development environments.

ContainDS Solutions will:

- Grant decision makers and clients easy access to actionable insights helping them move projects forward quickly and with confidence.
- Save time and reduce errors for your Data Science team, allowing them to focus on their core roles.
- Eliminate IT security threats from data science teams hosting web apps and sensitive data in arbitrary insecure cloud locations.
- Empower data scientists to use their dashboarding framework of choice while unifying your team’s approach to publishing.

ContainDS Dashboards is an extension for JupyterHub that allows users to instantly publish notebooks and other source code files 
as user-friendly interactive dashboards to share with non-technical colleagues.

Currently supports:

- Jupyter notebooks (`Voila <https://github.com/voila-dashboards/voila>`__)
- `Streamlit <https://streamlit.io/>`__ apps
- `Plotly Dash <https://plotly.com/dash/>`__ apps

Any authorised JupyterHub user can view the dashboard. This means that you can protect the dashboard with any authentication that works 
with JupyterHub - including single-sign-on through corporate email accounts or LDAP.

How it works
~~~~~~~~~~~~

- Data scientist creates a Jupyter Notebook as normal, or uploads Streamlit / Plotly Dash python files to Jupyter
- Data scientist creates a new Dashboard to clone their Jupyter server
- Other logged-in JupyterHub users see the dashboard in their list
- Click to launch as a server, using OAuth to gain access
- User sees a safe user-friendly version of the original notebook

All of this works through a new Dashboards menu item added to JupyterHub's header.

Data scientist creates a Jupyter Notebook as normal

.. figure:: ../_static/screenshots/1_Original_Jupyter_Notebook.png
   :alt: Screenshot of Original Jupyter Notebook

   
Data scientist creates a new Dashboard to clone their Jupyter server

.. figure:: ../_static/screenshots/2_Create_New_Dashboard.png
   :alt: Screenshot of Create New Dashboard


Other logged-in JupyterHub users see the dashboard in their list

.. figure:: ../_static/screenshots/3_Other_User_sees_dashboard.png
   :alt: Screenshot of Other User sees dashboard


Click to launch as a server - Dashboard Voila built automatically

.. figure:: ../_static/screenshots/4_Dashboard_Voila_built_automatically.png
   :alt: Screenshot of Dashboard Voila built automatically


Uses OAuth to gain access

.. figure:: ../_static/screenshots/5_Other_user_OAuths.png
   :alt: Screenshot of Uses OAuth to gain access


Other user sees a safe user-friendly Voila version of the original notebook

.. figure:: ../_static/screenshots/6_Voila_Dashboard.png
   :alt: Screenshot of Voila Dashboard

More details on how this works are in the :ref:`user guide<userguide>`, or you can find out :ref:`how to install<setup>` ContainDS Dashboards.

# ContainDS Dashboards for JupyterHub

A Dashboard publishing solution for Data Science teams to share results with decision makers.

Run a private on-premise or cloud-based JupyterHub with extensions to instantly publish Jupyter notebooks or Streamlit apps as 
user-friendly interactive dashboards to share with non-technical colleagues.

This open source package allows users to create interactive Jupyter notebooks that can be instantly and reliably published as 
secure interactive [Voila](https://voila.readthedocs.io/en/stable/) web apps.

Any authorised JupyterHub user can view the dashboard.

See [full documentation](https://cdsdashboards.readthedocs.io/en/stable/).

## How it works

- Data scientist creates a Jupyter Notebook as normal or uploads Streamlit Python files
- Data scientist creates a new Dashboard to clone their Jupyter server
- Other logged-in JupyterHub users see the dashboard in their list
- Click to launch as a server, using OAuth to gain access
- User sees a safe user-friendly Voila version of the original notebook

All of this works through a new Dashboards menu item added to JupyterHub's header.

_Data scientist creates a Jupyter Notebook as normal_

![Original Jupyter Notebook](./docs/_static/screenshots/1_Original_Jupyter_Notebook.png "Original Jupyter Notebook")

_Data scientist creates a new Dashboard to clone their Jupyter server_

![Create New Dashboard](./docs/_static/screenshots/2_Create_New_Dashboard.png "Create New Dashboard")


_Other logged-in JupyterHub users see the dashboard in their list_

![Other User sees dashboard](./docs/_static/screenshots/3_Other_User_sees_dashboard.png "Other User sees dashboard")

_Click to launch as a server_

![Dashboard Voila built automatically](./docs/_static/screenshots/4_Dashboard_Voila_built_automatically.png "Dashboard Voila built automatically")

_Uses OAuth to gain access_

![Other user OAuths](./docs/_static/screenshots/5_Other_user_OAuths.png "Other user OAuths")

_Other user sees a safe user-friendly Voila version of the original notebook_

![Voila Dashboard](./docs/_static/screenshots/6_Voila_Dashboard.png "Voila Dashboard")

_Or a Streamlit app_

![Streamlit App](./docs/_static/screenshots/7_Streamlit_App.png "Streamlit App")


## Requirements

Basic requirements:

- JupyterHub 1.0+
- Python 3.6+

You should be able to use any authenticator for users to login - for example, corporate Google email sign in, or LDAP.

Your JupyterHub will ideally be using LocalProcessSpawner (the default for standard installs), SystemdSpawner (default for The Littlest JupyterHub), 
or DockerSpawner.

Support for Kubernetes JupyterHub installations running KubeSpawner is in development - please get in touch with your requirements to help move this forward.

## Installation

Full [Setup and Installation details](https://cdsdashboards.readthedocs.io/en/stable/chapters/setup/setup.html) are in the documentation.

## Contact and Support

This software is an alpha version. Please see LICENSE for details.

Please do get in touch if you try out the package, or would like to but need some support. I would be very interested to find out how it can be used, and to work (without charge) to help you get it running. The project needs feedback in order to develop further!

For more background on this project and our related ContainDS Desktop product, please see our website: [containds.com](https://containds.com/).

Contact [support@containds.com](mailto:support@containds.com) with any comments or questions at all. Thank you.

[![Documentation Status](https://readthedocs.org/projects/cdsdashboards/badge/?version=stable)](https://cdsdashboards.readthedocs.io/en/stable/?badge=stable)

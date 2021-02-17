.. _upgrading:

Upgrading
---------

When a new version of ContainDS Dashboards or related components is released, the upgrade process may depend on your JupyterHub configuration.

Please see any specific notes in the :ref:`changelog` - for example, changes may be required to your jupyterhub_config.py file.

In general, you just need to remember to upgrade both your hub and user environments. If you only have one environment in your installation, you 
should run *both* the hub and user upgrade commands in your environment.

Especially in containerised environments (Docker or Kubernetes), existing singleuser servers may need to be deleted. They can be recreated by re-accessing 
the dashboard through the Dashboards page.

    **Sponsorship**

    If you are using ContainDS Dashboards in production please consider subscribing to a support plan.

    This will back future development of the 
    project and is a great way to satisfy your business stakeholders that you are adopting sustainable and supported software.

    It also helps you reach your corporate social responsibility goals since our open source software is used by academic and non-profit organizations. 
    
    More `Sponsorship details are on GitHub <https://github.com/sponsors/ideonate>`__.


LocalProcessSpawner or SystemdSpawner
=====================================

In the hub environment:


.. parsed-literal::

    pip install --upgrade cdsdashboards==\ |cds_version|
    # or
    conda install -c conda-forge cdsdashboards=\ |cds_version|


Also upgrade in the user environment, with some extra dependencies:


.. parsed-literal::

    pip install --upgrade cdsdashboards[user]==\ |cds_version|
    # or
    conda install -c conda-forge cdsdashboards-singleuser=\ |cds_version|


DockerSpawner
=============

In the hub environment:

.. parsed-literal::

    pip install --upgrade cdsdashboards==\ |cds_version|
    # or
    conda install -c conda-forge cdsdashboards=\ |cds_version|


Your singleuser image will also need to be upgraded.

For example, if using a pre-built image, in your jupyterhub_config.py:

.. parsed-literal::

    c.DockerSpawner.image = 'ideonate/containds-allr-datascience:|cds_version|'


If you are using your own image, please rebuild it, specifying the updated 
version numbers where appropriate.

The Littlest JupyterHub
=======================

Upgrade the cdsdashboards package in the hub environment:

.. parsed-literal::

    sudo -E /opt/tljh/hub/bin/python3 -m pip install cdsdashboards==\ |cds_version| 


Also upgrade cdsdashboards in the user environment, including extra dependencies:

.. parsed-literal::

    sudo -E /opt/tljh/user/bin/python3 -m pip install cdsdashboards[user]==\ |cds_version| 


Kubernetes (Z2JH)
=================

In your config.yaml file, update to the latest tags of the images used - both hub and singleuser.

Here is an example snippet from a config.yaml:

.. parsed-literal::

    hub:
      allowNamedServers: true
      image:
        name: ideonate/cdsdashboards-jupyter-k8s-hub
        tag: |z2jh_helm_version|-|cds_version|
    
    ...
    
    singleuser:
      image:
        name: ideonate/containds-allr-datascience
        tag: |cds_version|
    

If you are using your own images, please rebuild them, specifying the updated 
version numbers where appropriate.


Troubleshooting
===============

If you have any problems at all please :ref:`contact us <contact>` or open an 
issue on the `GitHub repo <https://github.com/ideonate/cdsdashboards/issues>`__. 
Be sure to describe your current configuration and 
any errors you are seeing.

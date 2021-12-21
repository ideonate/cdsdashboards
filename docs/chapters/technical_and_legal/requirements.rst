.. _requirements:

Requirements
------------

ContainDS Dashboards requires JupyterHub 1.x installed under Python 3.6+.

Note that JupyterHub 2.x is not supported. You will need to install a version 1.x (e.g. 1.5).

JupyterHub should ideally be configured with LocalProcessSpawner, SystemdSpawner, DockerSpawner, or KubeSpawner.

`The Littlest JupyterHub <http://tljh.jupyter.org/en/latest/>`__ (TLJH) is supported.

`Zero to JupyterHub on Kubernetes <http://z2jh.jupyter.org/>`__ is supported. Features available may depend on the persistent storage types available 
to you, as discussed in :ref:`z2jh setup <z2jh_pv>`.

It is also possible to use your own custom `installation of JupyterHub <https://jupyterhub.readthedocs.io/en/stable/installation-guide.html>`__.

.. _setup:

Setup
-----

First of all, you will need to install JupyterHub on your server.

If you aren't sure which installation type is best for you, please :ref:`get in touch<contact>` and we can help. 

For a straightforward single-machine setup try `The Littlest JupyterHub <http://tljh.jupyter.org/en/latest/>`__.

To scale for many users, try the Kubernetes-based `Zero to JupyterHub on Kubernetes <http://z2jh.jupyter.org/>`__.


It is also possible to attempt your own direct installation of JupyterHub. See 
the `instructions on JupyterHub's website <https://jupyterhub.readthedocs.io/en/stable/installation-guide.html>`__.


During JupyterHub configuration, you may need to choose a 'spawner' type - the way in which new Jupyter notebook environments are run for new users. 
Your setup can use the default LocalProcessSpawner, SystemdSpawner, DockerSpawner, or KubeSpawner.

It should be possible to use other spawner types and configurations - please :ref:`contact us<contact>` for assistance.

Once JupyterHub is running, please continue based on the spawner or installation type you are using:

.. toctree::
   :maxdepth: 2
   :caption: Setup:

   localprocess
   tljh
   docker
   z2jh
   otherspawners




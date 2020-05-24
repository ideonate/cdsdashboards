.. _setup:

Setup
-----

First of all, you will need to install JupyterHub on your server. Please follow 
the `instructions on JupyterHub's website <https://jupyterhub.readthedocs.io/en/stable/installation-guide.html>`__.

Kubernetes is not currently supported.

If you aren't sure which installation type is best for you, please :ref:`get in touch<contact>` and we can help. 
Or try `The Littlest JupyterHub <http://tljh.jupyter.org/en/latest/>`__.

During JupyterHub configuration, you may need to choose a 'spawner' type - the way in which new Jupyter notebook environments are run for new users 


Your setup can use the default LocalProcessSpawner, or you can choose to use DockerSpawner.

The Docker alternative means your users' computing environments are cleanly containerised (so separate from the rest of your server). It also means 
that the user's file tree can be easily cloned into a new dashboard.

Once JupyterHub is running, using either DockerSpawner or LocalProcessSpawner (or similar), please continue based on the spawner type you are using:

.. toctree::
   :maxdepth: 1
   :caption: Setup:

   localprocess
   docker




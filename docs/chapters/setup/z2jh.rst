.. _z2jh:


Kubernetes (Z2JH)
=================

Basing your JupyterHub installation on `Kubernetes <https://kubernetes.io/>`__ allows you to scale across multiple machines to support many users.

The most popular way to deploy JupyterHub on Kubernetes (k8s) is using `Zero to JupyterHub <http://z2jh.jupyter.org/>`__ (z2jh). This 
provides a template-driven approach to ensuring that you can change configuration values that are important to you while leaving most of the setup 
to carefully-chosen defaults from z2jh.

In this guide, we will assume you are using z2jh, but you should be able to adapt the instructions for other k8s-based deployments.

Some configuration choices will be made when setting up your JupyterHub, and these will depend on the cloud provider or hosting infrastructure you 
are using, as well as on your particular needs from the JupyterHub.

Please note that some configuration choices, especially in regards to persistent storage, may mean that different workarounds are needed in order 
for ContainDS Dashboards to work properly. You are encouraged to :ref:`get in touch<contact>` to discuss your own situation, and this may guide 
development of the product and documentation for others going forward.

General Installation
~~~~~~~~~~~~~~~~~~~~

We assume you have already followed `z2jh instructions <https://zero-to-jupyterhub.readthedocs.io/en/latest/index.html>`__ to set up a JupyterHub.

The cdsdashboards package needs to be installed on your hub image, or accessible to it somehow.

The easiest solution is just to use our public Docker image instead of the default `jupyterhub/k8s-hub <https://hub.docker.com/r/jupyterhub/k8s-hub>`__ 
provided by z2jh. Our image is called `ideonate/cdsdashboards-jupyter-k8s-hub <https://hub.docker.com/r/ideonate/cdsdashboards-jupyter-k8s-hub>`__, and simply 
has cdsdashboards installed on top of the base jupyterhub/k8s-hub image.

If you are already using your own custom image for the hub, you may need to build on top of that 
in a similar way to `our example Dockerfile <https://github.com/ideonate/cdsdashboards/blob/master/docker-images/z2jh/hub/Dockerfile.pypi>`__.

Currently, we build on top of the most recent Helm chart available (see corresponding 
`components and requirements <https://github.com/jupyterhub/helm-chart#versions-coupled-to-each-chart-release>`__).

Our ideonate/cdsdashboards-jupyter-k8s-hub image is tagged as, for example, '|z2jh_helm_version|-|cds_version|' meaning it is based on the z2jh version 
|z2jh_helm_version| and containing cdsdashboards version |cds_version|.

As well as setting the new hub image, you will also need a compatible 'singleuser' image, fulfilling the same 
:ref:`requirements as for DockerSpawner <docker_singleuser_image>`. A suitable starting point is one of 
`our examples <https://github.com/ideonate/cdsdashboards-jupyter-docker>`__.

config.yaml
-----------

Merge the following settings in to your deployment's config.yaml file.

.. parsed-literal::

    hub:
      allowNamedServers: true
      image:
        name: ideonate/cdsdashboards-jupyter-k8s-hub
        tag: |z2jh_helm_version|-|cds_version|
      extraConfig:
        cds-handlers: |
          from cdsdashboards.hubextension import cds_extra_handlers
          c.JupyterHub.extra_handlers = cds_extra_handlers
        cds-templates: |
          from cdsdashboards.app import CDS_TEMPLATE_PATHS
          c.JupyterHub.template_paths = CDS_TEMPLATE_PATHS
        cds-kube: |
          c.JupyterHub.spawner_class = 'cdsdashboards.hubextension.spawners.variablekube.VariableKubeSpawner'
          c.CDSDashboardsConfig.builder_class = 'cdsdashboards.builder.kubebuilder.KubeBuilder'

    singleuser:
      image:
        name: ideonate/containds-allr-datascience
        tag: |cds_version|

The hub.image and singleuser.image settings have already been discussed. In addition, we enable 
`named servers <https://jupyterhub.readthedocs.io/en/stable/reference/config-user-env.html#named-servers>`__, and set some bespoke 
configuration to import ContainDS Dashboards (cdsdashboards). Note we are now using a slightly modified version of the KubeSpawner that 
knows how to present dashboards as well as regular Jupyter servers.

At this point, if you 
`apply configuration changes <https://zero-to-jupyterhub.readthedocs.io/en/latest/customizing/extending-jupyterhub.html#applying-configuration-changes>`__ 
you should see the new Dashboards menu in JupyterHub, but you may not be able to produce working dashboards unless your persistent storage configuration 
happens to be compatible already.


.. _z2jh_pv:


Persistent Storage
~~~~~~~~~~~~~~~~~~

There are two main ways to set up persistent user storage in z2jh: dynamic or static.

**Static storage** is where you create one large storage device which contains a home folder for every user, and any new Jupyter server mounts the user's home 
folder when it starts up. An example is using `ElasticFileSystem on AWS <https://zero-to-jupyterhub.readthedocs.io/en/latest/amazon/efs_storage.html>`__.

**Dynamic storage** (the default) is where a new 'persistent volume' is generally created for each new Jupyter server that starts up.

When a user creates a new Dashboard, it will be based within a new named server. The Dashboard is really just a 
new separate Jupyter server that happens to be running a presentation front-end (e.g. Voilà) instead of the usual Jupyter notebook server. We just 
need to ensure that required files (e.g. ipynb notebooks or py/R files) for the dashbboard are present on the new dashboard server.

The dashboard's source files can come from the Jupyter Tree or a Git Repo (:ref:`read more here <prepare_dashboard>`).

If you are creating dashboards based on a Git Repo, the source files will be pulled from the repo when the dashboard server is started, so any type of storage 
should be suitable.

If your dashboards are based on files in the user's Jupyter Tree, then you will need to ensure files uploaded to another Jupyter Server (e.g. the default 
'My Server') will also be available to the new dashboard server.

The easiest way to achieve this is to ensure that each user has their own home folder (or shared folder) that is somehow mounted on all of their servers.

Static Storage
--------------

If you are using static storage, this will probably work fine already - the default setup is for each user to have exactly one home folder that is 
mounted on all of their servers. So the dashboard server will pick up the same files as the source server. Here is typical config from your 
config.yaml:

::

    singleuser:

      storage:
        type: static
        static:
          pvcName: 'mypersistentvol-claim'
          subPath: 'home/{username}'

Great! However, there may be pros and cons to using static storage in your hosting scenario, or it may not be available at all.

Dynamic Storage
---------------

The default storage type is 'dynamic', and for each new *server* to have its own new persistent volume attached. Since new storage is created for a 
dashboard server, it starts off empty and does not contain the same files as the source server. So our dashboard files will not be found.

There are considered to be two main approaches at the moment:

- Ensure the user just has one storage volume that is attached to all their servers. (Per-User Storage)
- Clone the contents of the source server's volume into the new dashboard server. (Cloned Volumes)

However, the availability of these approaches may depend on the functionality available from your k8s installation.

Per-User Storage
++++++++++++++++

Ensuring the same volume is attached to each server is a simple configuration change, but it requires your persistent storage volumes to allow 
the 'ReadWriteMany' access type. (The z2jh default is 'ReadWriteOnce' which is more widely supported but only allows the volume to be mounted on 
one pod at a time.)

The following can be merged into your config.yaml:

::

    singleuser:
      storage:
        type: dynamic
        capacity: 10Gi
        dynamic:
          pvcNameTemplate: claim-{username}
          volumeNameTemplate: volume-{username}
          storageAccessModes: [ReadWriteMany]

The z2jh defaults are e.g. :code:`pvcNameTemplate: volume-{username}{servername}` which is why a new volume is created for each dashboard server too (it is 
dependent on servername *and* username, not just username as we require in the config above).

If you 
`apply configuration changes <https://zero-to-jupyterhub.readthedocs.io/en/latest/customizing/extending-jupyterhub.html#applying-configuration-changes>`__, 
new servers will be mounted in this new ReadWriteMany mode. However, any existing running servers will still be in ReadWriteOnce mode, and will need to be 
restarted before things will work - a volume can not be mounted in a mixture of ReadWriteMany and ReadWriteOnce modes at the same time.

Cloned Volumes
++++++++++++++

If ReadWriteMany mode is not available for your persistent volume type, it may be possible to use ReadWriteOnce with separate volumes for each server, but to 
instruct ContainDS Dashboards to clone the contents of the source server's volume whenever a new dashboard is created. Of course, this also results in a different 
experience for your user - changes in the source server can not be reflected in the dashboard server unless it is rebuilt.

This `functionality requires Kubernetes 1.16+ <https://kubernetes.io/docs/concepts/storage/volume-pvc-datasource/>`__ and is not available in all persistent 
storage drivers. At present, this approach is considered experimental, and you are encouraged to :ref:`get in touch<contact>` for help in understanding if this 
approach will work for you.


Hybrid Static/Dynamic
---------------------

If you feel unable to use Static Storage because it slows down your JupyterLab sessions too much, but don't have a suitable way to share files between Dynamic 
volumes, then a hybrid approach might work.

Your primary persistent storage might be through a dynamic PVC in ReadWriteOnce mode, but you also share a secondary static storage volume:

::

    singleuser:
      storage:
        extraVolumes:
        - name: shared
          persistentVolumeClaim: 
            claimName: shared-claim
        extraVolumeMounts:
        - name: shared
          mountPath: /home/jovyan/shared

In this scenario, you can instruct your users to use the *shared* folder within Jupyter to hold their dashboard files - perhaps within a further *<username>* 
folder. This way, all dashboard files will be available to all servers, including the dashboard server - and also in their colleagues' own servers too, of 
course.

Options
~~~~~~~

Extra options to control behavior of Dashboards are available. The universal approach for setting these in z2jh is to add extraConfig lines.

For example:

::

    extraConfig:
      cds-options: |
        c.CDSDashboardsConfig.presentation_types = ['voila']

See details of the :ref:`customization` available.


Future Development
~~~~~~~~~~~~~~~~~~

JupyterHubs on Kubernetes can come in many different configurations, and on varied infrastructure. It is our goal to understand as many of these as 
possible, and to help simplify set up of ContainDS Dashboards in new circumstances. 

You are strongly encouraged to :ref:`let us know<contact>` how the guidance here has worked for you (good or bad), and to help us adapt or think of new 
approaches to your circumstances.

Please `sign up to the ContainDS email list <https://containds.com/signup/>`__ to receive notifications about updates to the project including new 
features and security advice.

Sponsorship
~~~~~~~~~~~

If you are using ContainDS Dashboards in production please consider subscribing to a support plan.

This will back future development of the 
project and is a great way to satisfy your business stakeholders that you are adopting sustainable and supported software.

It also helps you reach your corporate social responsibility goals since our open source software is used by academic and non-profit organizations. 

More `Sponsorship details are on GitHub <https://github.com/sponsors/ideonate>`__.
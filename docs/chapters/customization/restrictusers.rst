.. _restrictusers:


Restrict which Users can Spawn Servers and Dashboards
=====================================================

Non-technical users may be added to your JupyterHub in order to view dashboards created by data scientists, but you 
may not want those users to be able to spawn Jupyter servers or create their own Dashboards.

By default, all JupyterHub users can perform both those operations, but it is possible to restrict these abilities 
only to specified users. This can be controlled by setting JupyterHub Group memberships.

There are two possible choices: specify an 'allow list' group of users who can spawn servers (and dashboards) or 
specify a 'block list' of users who cannot. The allow list approach is generally more secure (new users will be 
unable to spawn by default) but may not be convenient if most new users will be data scientists.

In your jupyterhub_config.py or equivalent add:
:code:`c.CDSDashboardsConfig.spawn_allow_group = 'spawners-group'`
(or whatever group name you want - it will be created if it doesn't exist).
Users must belong to this group to be allowed to spawn servers or create dashboards.

Alternatively use:
:code:`c.CDSDashboardsConfig.spawn_block_group = 'viewers-group'`
(or any choice of group name) 
to specify a list of users who should only be viewers and thus unable to spawn servers.

If spawn_block_group is blank, spawn_allow_group will determine which users should be able to spawn.
If both settings are blank, all users will be allowed to spawn.
If both are non-blank, spawn_block_group will take priority (i.e. spawn_allow_group will be ignored).


Managing Groups
---------------

Groups are a relatively well-hidden feature of JupyterHub. There is a REST API to manage group membersip, and 
ContainDS Dashboards also adds a user interface so that admins can manage group membership interactively.

In the Admin page of JupyterHub (with ContainDS Dashboards installed), there should be a 'Manage Groups' link 
towards the top of the page. Any admin 
user can use that to add/remove users to the 'spawners-group' or 'viewers-group'.

Updating the JupyterHub UI
--------------------------

Use of spawn_block_group/spawn_allow_group will ensure forbidden users cannot ultimately carry out restricted actions. 
However, users may still be able to see the big blue 'My Server' button on the home page, or might even be redirected 
into the spawn page by default when they login - only to see an error when this fails, saying they do not have permissions.

To ensure a more pleasant experience, there is an alternative set of page templates that can be used.

In your jupyterhub_config.py or equivalent, replace these lines:

::

    from cdsdashboards.app import CDS_TEMPLATE_PATHS
    c.JupyterHub.template_paths = CDS_TEMPLATE_PATHS

with:

::

    from cdsdashboards.app import CDS_TEMPLATE_PATHS_RESTRICTED
    c.JupyterHub.template_paths = CDS_TEMPLATE_PATHS_RESTRICTED

These templates link the Home entry in the menu bar to a bespoke version of /hub/home located instead at /hub/home-cds which 
provides a polite message to users who are not allowed to spawn (in place of the 'My Server' button).

It is still possible for the user to access /hub/home by URL directly should they decide to do so.

To ensure the user is not automatically redirected to the spawn or (real) home page on login, it is also highly recommended 
that you carry out the steps suggested in :ref:`finetune`.

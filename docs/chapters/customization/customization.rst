.. _customization:

Customization
-------------

Once initial setup is complete, there are further customizations you may want to make.

:ref:`huboptions` covers settings of ContainDS Dashboards that change what users can see and do in JupyterHub. For example, you can 
hide the 'named servers' section on the home page, and restrict which 'presentation types' (frameworks such as Voilà, Streamlit, etc.) 
that should be available for Dashboards.

:ref:`useroptions` covers settings affecting individual dashboard servers (spawner config).

:ref:`finetune` explores generic JupyterHub settings that may make sense now that you have non-technical users logging in. For example, 
launching straight into 'My Server' may not be the best landing page for those users.

To tighten this up further, you can :ref:`restrictusers`. 

:ref:`github` explains how to integrate with GitHub for easy login and/or to easily pull from private repos straight into dashboards 
(and Jupyter notebook environments too).

:ref:`customlaunchers` is an advanced topic explaining how you can add your own presentation types (frameworks) or adjust the way that 
the built-in presentation servers are launched.


.. toctree::
   :maxdepth: 1
   :caption: Customization:

   huboptions
   useroptions
   finetune
   restrictusers
   github
   customlaunchers
   
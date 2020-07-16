.. _working:

Working with Dashboards
-----------------------

This section explains how your Dashboard operates, and can be shared with other users.

It presumes you have already created a Dashboard following one of:

- :ref:`voila`
- :ref:`streamlit`
- :ref:`plotlydash`
- :ref:`bokehpanel`
- :ref:`rshiny`

Running and Rebuilding Dashboards
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Back in the Home page in JupyterHub, you can see that the Dashboard is really just running a new Jupyter server (albeit one runnning Voila instead 
of the regular Jupyter server):

.. figure:: ../../../../_static/screenshots/userguide/working/DashboardNamedServer.png
   :alt: Dashboard Named Server

You can try Stopping (and optionally Deleting) this server. If you then go to Dashboards you can still see the Dashboard definition:

.. figure:: ../../../../_static/screenshots/userguide/working/DashboardListOne.png
   :alt: Dashboard List showing our one dashboard

If you then click into the View URL, the Dashboard will build again, then you can click 'Go to Dashboard' once ready just as before.

A Dashboard will also be forced to rebuid if you edit it for any reason.

Editing a Dashboard
~~~~~~~~~~~~~~~~~~~

.. figure:: ../../../../_static/screenshots/userguide/working/DashboardListOne.png
   :alt: Dashboard List showing our one dashboard

From the Dashboards page, click 'edit' by the dashboard to see its definition again:

.. figure:: ../../../../_static/screenshots/userguide/working/EditDashboard.png
   :alt: Dashboard Edit

You can change any of the settings, e.g. Description to change the text seen by others when they first click on the Dashboard in their 
own list (see below). Or you might need to change the 'Path to a file or folder'.

When you click Save the dashboard will be rebuilt as it was when you first set up the Dashboard definition.

Sharing a Dashboard
~~~~~~~~~~~~~~~~~~~

The Dashboard is automatically accessible to any other authenticated user.

If another user clicks on the Dashboards menu in JupyterHub, they will be able to see your Dashboards:

.. figure:: ../../../../_static/screenshots/userguide/working/OthersDashboards.png
   :alt: Dashboards List

If they click on your Dashboard's name they will see the summary screen, just as you did when you first built the Dashboard:

.. figure:: ../../../../_static/screenshots/userguide/working/OthersSummary.png
   :alt: Dashboard Summary

In the case above, the Dashboard was already built and running, so it only remains for the user to click 'Go to Dashboard'. If the 
dashboard server had been stopped or deleted, the other user would be able to see the Dashboard being restarted and/or rebuilt, along 
with any error message if there was a problem.

Since it is not their server, ContainDS Dashboards will require the other user to authenticate into your server:

.. figure:: ../../../../_static/screenshots/userguide/working/OthersOAuth.png
   :alt: OAuth screen

When they accept, they will be able to see the results. Here is a Voila (Jupyter notebook) Dashboard:

.. figure:: ../../../../_static/screenshots/userguide/working/OthersResults.png
   :alt: Other User sees Voila Dashboard

And here is a Streamlit app:

.. figure:: ../../../../_static/screenshots/userguide/working/OthersStreamlitApp.png
   :alt: Other User sees Streamlit Dashboard

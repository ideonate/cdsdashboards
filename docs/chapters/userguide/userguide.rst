.. _userguide:

User Guide
----------

Dashboards menu
~~~~~~~~~~~~~~~

Once :ref:`setup<setup>` your JupyterHub have a new Dashboards menu. It will also have a Named Server section if this wasn't enabled 
previously (or hidden in :ref:`options<options>`).

.. figure:: ../../_static/screenshots/userguide/NamedServers.png
   :alt: JupyterHub with Dashboards

Developing a Dashboard
~~~~~~~~~~~~~~~~~~~~~~

Dashboards can be created based on Jupyter notebooks or py or R files.

Use 'My Server' (or a named server) to create a Jupyter notebook (ipynb file) as normal or upload/edit Python or R files to make apps.

Below, we have both an ipynb (Jupyter notebook) and a py file. We will be able to make two dashboards, one for each file.

.. figure:: ../../_static/screenshots/userguide/JupyterTree.png
   :alt: Jupyter with ipynb and py files

For Jupyter notebooks, of course you can run them as usual in your Jupyter server - and there is a 'Voila Preview' button so you can see how 
the final dashboard will appear. Voila is the name of the technology that is essentially a user-friendly and secure version of Jupyter notebooks: 
code cells are hidden, and the user can only view the intended end result. They can interact with widgets if they are present in the notebook though.

Streamlit, Plotly Dash, Bokeh/Panel, and R Shiny apps can't normally be run at this stage (in Jupyter), so for now you would upload Python/R files 
and data that you have developed on your own machine.

Follow Jupyter (Voila), Streamlit, Plotly Dash, Bokeh / Panel, or R Shiny below for details on turning your code into a Dashboard to share with colleagues:

.. toctree::
   :maxdepth: 1

   voila
   streamlit
   plotlydash
   bokehpanel
   rshiny
   working



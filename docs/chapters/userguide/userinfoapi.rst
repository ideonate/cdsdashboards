.. _userinfoapi:

API for User Info
-----------------

**Experimental Feature**

Users' dashboards built in Voilà, Streamlit, Plotly Dash etc may benefit from knowing which JupyterHub user is currently accessing the 
dashboard, along with other information about them.

There is a simple API available to obtain this within a dashboard notebook or Python script etc, for example in Javascript:

::

    fetch(
        '/hub/dashboards-api/hub-info/user',
        { 
            mode: 'no-cors', 
            credentials: 'same-origin',
            headers: new Headers({'Access-Control-Allow-Origin':'*'}) 
        }
    );

This should return JSON something like:

::

    {'kind': 'user',
    'name': 'dan',
    'admin': True,
    'groups': ['spawners-group'],
    'server': '/user/dan/', /* Just their default 'My Server' */
    'pending': None,
    'created': '2020-06-10T15:00:51.975826Z',
    'last_activity': '2020-12-16T09:40:59.163744Z',
    'servers': None}

An explanation of how this could be used in Voilà is `in this Gist <https://gist.github.com/danlester/ac1d5f29358ce1950482f8e7d4301f86>`__.

It is possible to instruct the User Info API to return extra information by adding some configuration to jupyterhub_config:

- include_auth_state
- include_servers
- include_servers_state

More details are :ref:`here<userinfoapi_settings>`.

These should all be considered very carefully from a security point of view, depending on your overall JupyterHub configuration.

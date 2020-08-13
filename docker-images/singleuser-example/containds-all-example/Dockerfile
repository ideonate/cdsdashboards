ARG TAG=1.2
ARG BASE_REPO=jupyterhub/singleuser

FROM $BASE_REPO:$TAG

# git is now used to source files for cdsdashboards
RUN conda install --quiet --yes -c conda-forge git

RUN rm -rf /home/jovyan/work

# Effectively we just want to run
# RUN pip install cdsdashboards[user]
# But we often build the docker image before the cdsdashboards release to pypi
# so just pick the bits we need:

ARG JHSINGLENATIVEPROXY_LINE=jhsingle-native-proxy>=0.4.0

RUN pip install $JHSINGLENATIVEPROXY_LINE plotlydash-tornado-cmd>=0.0.4 bokeh-root-cmd>=0.0.5 rshiny-server-cmd>=0.0.2 voila-materialstream>=0.2.6

# Install the frameworks

ARG FRAMEWORKS_LINE="voila streamlit dash bokeh panel holoviews"

RUN pip install $FRAMEWORKS_LINE

# Set the voila default template

USER $NB_UID
COPY jupyter_notebook_config_extra.py /etc/jupyter/
RUN cat /etc/jupyter/jupyter_notebook_config_extra.py >> /etc/jupyter/jupyter_notebook_config.py
RUN rm /etc/jupyter/jupyter_notebook_config_extra.py

COPY voila.json /etc/jupyter

# Enable local conda envs

RUN conda init bash

# Startup hook for obtaining GitHub OAuth tokens and user details

COPY github-tokens.sh /usr/local/bin/before-notebook.d/github-tokens.sh


# Fix permissions on /etc/jupyter as root
USER root
RUN fix-permissions /etc/jupyter/



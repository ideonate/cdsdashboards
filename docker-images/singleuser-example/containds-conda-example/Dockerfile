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

ARG JHSINGLENATIVEPROXY_LINE=jhsingle-native-proxy>=0.6.1

RUN pip install $JHSINGLENATIVEPROXY_LINE plotlydash-tornado-cmd>=0.0.4 bokeh-root-cmd>=0.1.2 rshiny-server-cmd>=0.0.2 voila-materialstream>=0.2.6

# Install the frameworks

ARG FRAMEWORKS_LINE="voila streamlit"

RUN pip install $FRAMEWORKS_LINE

# Install Voila and ContainDS JupyterLab extensions

USER $NB_UID

RUN jupyter labextension install @jupyter-voila/jupyterlab-preview @ideonate/jupyter-containds

# Fix permissions on /etc/jupyter as root
USER root
RUN fix-permissions /etc/jupyter/


# Enable local conda envs

USER $NB_UID
COPY .condarc /etc/conda/.condarc

RUN conda init bash
# But the changes made in /home/jovyan will be clobbered when we mount a persistent volume
COPY conda-init.sh /etc/profile.d/conda-init.sh




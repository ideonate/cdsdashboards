ARG TAG=1.2
ARG BASE_REPO=jupyterhub/singleuser

FROM $BASE_REPO:$TAG

# git is now used to source files for cdsdashboards
RUN conda install --quiet --yes -c conda-forge git pip

RUN rm -rf /home/jovyan/work

# Effectively we just want to run
# RUN pip install cdsdashboards[user]
# But we often build the docker image before the cdsdashboards release to pypi
# so just pick the bits we need:

RUN pip install jhsingle-native-proxy>=0.6.1

# Install the frameworks

RUN pip install voila

# FASTAPI

RUN pip install fastapi==0.63.0 flask==1.1.2 jupyterhub==1.3.0 requests==2.25.1 typer==0.3.2 uvicorn==0.13.3


USER $NB_UID

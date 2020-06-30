ARG TAG=1.2
ARG BASE_REPO=jupyterhub/singleuser
FROM $BASE_REPO:$TAG

RUN rm -rf /home/jovyan/work

RUN conda install --quiet --yes -c conda-forge voila

RUN pip install cdsdashboards[user]

RUN pip install voila

RUN pip install streamlit

RUN pip install dash plotlydash-tornado-cmd

RUN pip install bokeh panel bokeh-root-cmd>=0.0.5

RUN pip install jhsingle-native-proxy>=0.3.2

COPY voila-entrypoint.sh /opt/conda/bin

COPY streamlit-entrypoint.sh /opt/conda/bin

COPY plotlydash-entrypoint.sh /opt/conda/bin

COPY bokeh-entrypoint.sh /opt/conda/bin

USER $NB_UID
COPY jupyter_notebook_config_extra.py /etc/jupyter/
RUN cat /etc/jupyter/jupyter_notebook_config_extra.py >> /etc/jupyter/jupyter_notebook_config.py
RUN rm /etc/jupyter/jupyter_notebook_config_extra.py

COPY voila.json /etc/jupyter


# Fix permissions on /etc/jupyter as root
USER root
RUN fix-permissions /etc/jupyter/
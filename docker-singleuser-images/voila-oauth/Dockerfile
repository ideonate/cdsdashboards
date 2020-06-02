ARG TAG=1.2
ARG BASE_REPO=jupyterhub/singleuser
FROM $BASE_REPO:$TAG

RUN rm -rf /home/jovyan/work

RUN conda install --quiet --yes -c conda-forge voila

RUN pip install jhsingle-native-proxy==0.1.3 voila-materialstream

RUN pip install streamlit

COPY voila-entrypoint.sh /opt/conda/bin

COPY streamlit-entrypoint.sh /opt/conda/bin


USER $NB_UID
COPY jupyter_notebook_config_extra.py /etc/jupyter/
RUN cat /etc/jupyter/jupyter_notebook_config_extra.py >> /etc/jupyter/jupyter_notebook_config.py
RUN rm /etc/jupyter/jupyter_notebook_config_extra.py

COPY voila.json /etc/jupyter


# Fix permissions on /etc/jupyter as root
USER root
RUN fix-permissions /etc/jupyter/
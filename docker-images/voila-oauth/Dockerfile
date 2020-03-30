ARG TAG=1.2
ARG BASE_REPO=jupyterhub/singleuser
FROM $BASE_REPO:$TAG

RUN conda install --quiet --yes -c conda-forge voila

RUN pip install jhsingle-native-proxy

COPY voila-entrypoint.sh /opt/conda/bin

ARG TAG=1.2
FROM jupyterhub/singleuser:$TAG

RUN conda install --quiet --yes -c conda-forge voila

COPY voila-entrypoint.sh /opt/conda/bin

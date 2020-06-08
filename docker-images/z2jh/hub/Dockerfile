FROM jupyterhub/k8s-hub:0.9.0

USER root

RUN python3 -m pip install --upgrade --no-cache cdsdashboards

USER ${NB_USER}

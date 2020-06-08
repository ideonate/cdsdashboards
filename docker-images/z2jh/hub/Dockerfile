FROM jupyterhub/k8s-hub:0.9.0

USER root

RUN mkdir /tmp/cdsdashboard_current

ADD . /tmp/cdsdashboard_current/

RUN cd /tmp/cdsdashboard_current \
        && python3 setup.py sdist \
        && python3 -m pip install ./`ls dist/cdsdashboards-*.tar.gz` \
        && cd .. && rm -rf ./cdsdashboard_current

USER ${NB_USER}

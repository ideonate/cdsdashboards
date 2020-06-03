ARG JUPYTERHUB_VERSION=1.2
FROM jupyterhub/jupyterhub:$JUPYTERHUB_VERSION

RUN mkdir /tmp/cdsdashboard_current

ADD . /tmp/cdsdashboard_current/

RUN cd /tmp/cdsdashboard_current && pip3 install -e .


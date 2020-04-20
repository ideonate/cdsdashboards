ARG JUPYTERHUB_VERSION
FROM jupyterhub/jupyterhub:$JUPYTERHUB_VERSION

# Install dockerspawner, oauth, postgres
RUN /usr/local/bin/pip install -q psycopg2-binary==2.8.5 && \
    /usr/local/bin/pip install -q PyMySQL==0.9.3 && \
    /usr/local/bin/pip install \
        oauthenticator==0.8.* \
        dockerspawner==0.11.*

RUN mkdir /tmp/cdsdashboard_current

ADD . /tmp/cdsdashboard_current/

RUN cd /tmp/cdsdashboard_current && pip3 install -e .

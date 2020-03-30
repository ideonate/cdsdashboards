ARG TAG=1.2
FROM ideonate/jh-voila-public-singleuser:$TAG

RUN pip install jhsingle-native-proxy

COPY voila-entrypoint.sh /opt/conda/bin

# cdsdashboards under docker compose

## Generate certs

Something like:

`openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout secrets/jupyterhub.key -out secrets/jupyterhub.crt`

## Build Hub Image including cdsdashboards (local)

`make hub_image build`

## Run the docker cluster

`docker-compose up`


# Behind nginx

`docker-compose -f docker-compose-nginx.yml up`

# nginx locally

To run nginx in a docker container, reverse-proxying to a locally-running JupyterHub instance:

``docker run -v `pwd`/nginx-local.conf:/etc/nginx/nginx.conf -v `pwd`/secrets/jupyterhub.crt:/data/cert.crt -v `pwd`/secrets/jupyterhub.key:/data/key.key -p 443:443 nginx``

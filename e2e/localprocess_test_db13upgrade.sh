#!/bin/bash

export JH_CYPRESS_BASE_IMAGE="jupyterhub/jupyterhub:1.2"

export JH_CYPRESS_DOCKERFILE="Dockerfile"

export JH_CYPRESS_JHCONFIG_SRC="/jh_cypress_config/localprocess_jupyterhub_config.py"
export JH_CYPRESS_JHCONFIG_DEST="/srv/jupyterhub/jupyterhub_config.py"

export JH_CYPRESS_SQLITE_SRC="/jh_cypress_config/from.0.0.13.sqlite"
export JH_CYPRESS_SQLITE_DEST="/srv/jupyterhub/jupyterhub.sqlite"

export JH_CYPRESS_HOME_SRC="/jh_cypress_config/userhome"
export JH_CYPRESS_HOME_DEST="/home"

export JH_CYPRESS_CREATE_USERS="dan"

# The DB upgrade is silent, so just check login
# People who attempted to install a fresh 0.0.13 faced this perpetual can't upgrade error. Future versions set them right.
export JH_CYPRESS_TESTS="/e2e/cypress/integration/login.spec.js"

export JH_CYPRESS_MEDIAFOLDER="local_db13upgrade"

docker-compose up --exit-code-from cypress --force-recreate
docker-compose down

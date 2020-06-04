#!/bin/bash

export JH_CYPRESS_BASE_IMAGE="ideonate/tljh-dev:20200604"

export JH_CYPRESS_DOCKERFILE="Dockerfile.tljh"

export JH_CYPRESS_JHCONFIG_SRC="/jh_cypress_config/tljh_jupyterhub_config.py"
export JH_CYPRESS_JHCONFIG_DEST="/opt/tljh/config/jupyterhub_config.d/cds_jupyterhub_config.py"

export JH_CYPRESS_SQLITE_SRC=""
export JH_CYPRESS_SQLITE_DEST=""

export JH_CYPRESS_HOME_SRC="/jh_cypress_config/userhome"
export JH_CYPRESS_HOME_DEST="/home"

export JH_CYPRESS_USER_PREFIX="jupyter-"
export JH_CYPRESS_CREATE_USERS="dan"

export JH_CYPRESS_TESTS="/e2e/cypress/integration/voila.spec.js"

export JH_CYPRESS_MEDIAFOLDER="tljh_voila"

docker-compose up --force-recreate --exit-code-from cypress 
docker-compose down

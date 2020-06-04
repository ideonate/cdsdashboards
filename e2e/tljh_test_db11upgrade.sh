#!/bin/bash

export JH_CYPRESS_BASE_IMAGE="ideonate/tljh-dev:20200604"

export JH_CYPRESS_DOCKERFILE="Dockerfile.tljh"

export JH_CYPRESS_JHCONFIG_SRC="/jh_cypress_config/tljh_jupyterhub_config.py"
export JH_CYPRESS_JHCONFIG_DEST="/opt/tljh/config/jupyterhub_config.d/cds_jupyterhub_config.py"

export JH_CYPRESS_SQLITE_SRC="/jh_cypress_config/from.0.0.11.sqlite"
export JH_CYPRESS_SQLITE_DEST="/opt/tljh/state/jupyterhub.sqlite"

export JH_CYPRESS_HOME_SRC="/jh_cypress_config/userhome"
export JH_CYPRESS_HOME_DEST="/home"

export JH_CYPRESS_USER_PREFIX="jupyter-"
export JH_CYPRESS_CREATE_USERS="dan"

export JH_CYPRESS_TESTS="/e2e/cypress/integration/dbupgrade.spec.js"

export JH_CYPRESS_MEDIAFOLDER="tljh_db11upgrade"

docker-compose up --exit-code-from cypress --force-recreate
docker-compose down

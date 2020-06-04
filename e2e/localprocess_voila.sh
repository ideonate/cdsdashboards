#!/bin/bash

export JH_CYPRESS_BASE_IMAGE="jupyterhub/jupyterhub:1.2"

export JH_CYPRESS_JHCONFIG_SRC="/jh_cypress_config/localprocess_jupyterhub_config.py"
export JH_CYPRESS_JHCONFIG_DEST="/srv/jupyterhub/jupyterhub_config.py"

export JH_CYPRESS_SQLITE_SRC=""
export JH_CYPRESS_SQLITE_DEST=""

export JH_CYPRESS_HOME_SRC="/jh_cypress_config/userhome/*"
export JH_CYPRESS_HOME_DEST="/home"

export JH_CYPRESS_CREATE_USERS="dan"

export JH_CYPRESS_TESTS="/e2e/cypress/integration/voila.spec.js"

export JH_CYPRESS_MEDIAFOLDER="local_voila"

docker-compose up #--exit-code-from cypress --force-recreate
#docker-compose down

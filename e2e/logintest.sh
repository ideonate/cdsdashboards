#!/bin/bash

export JH_CYPRESS_JHCONFIG_SRC="/jh_cypress_config/test_jupyterhub_config.py"
export JH_CYPRESS_JHCONFIG_DEST="/srv/jupyterhub/jupyterhub_config.py"

export JH_CYPRESS_SQLITE_SRC=""
export JH_CYPRESS_SQLITE_DEST=""

export JH_CYPRESS_TESTS="/e2e/cypress/integration/login.spec.js"

docker-compose up --exit-code-from cypress --force-recreate

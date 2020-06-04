#!/bin/bash

export JH_CYPRESS_BASE_IMAGE="ideonate/tljh-dev:20200604"

export JH_CYPRESS_DOCKERFILE="Dockerfile.tljh"

export JH_CYPRESS_JHCONFIG_SRC="/jh_cypress_config/tljh_jupyterhub_config.py"
export JH_CYPRESS_JHCONFIG_DEST="/opt/tljh/config/jupyterhub_config.d/cds_jupyterhub_config.py"

export JH_CYPRESS_SQLITE_SRC=""
export JH_CYPRESS_SQLITE_DEST="/opt/tljh/state/jupyterhub.sqlite"

export JH_CYPRESS_HOME_SRC="/jh_cypress_config/userhome"
export JH_CYPRESS_HOME_DEST="/home"

export JH_CYPRESS_USER_PREFIX="jupyter-"
export JH_CYPRESS_CREATE_USERS="dan"



#!/bin/bash

export JH_CYPRESS_BASE_IMAGE="jupyterhub/jupyterhub:1.2"

export JH_CYPRESS_DOCKERFILE="Dockerfile"

export JH_CYPRESS_JHCONFIG_SRC="/jh_cypress_config/localprocess_jupyterhub_config.py"
export JH_CYPRESS_JHCONFIG_DEST="/srv/jupyterhub/jupyterhub_config.py"

export JH_CYPRESS_SQLITE_SRC=""
export JH_CYPRESS_SQLITE_DEST="/srv/jupyterhub/jupyterhub.sqlite"

export JH_CYPRESS_HOME_SRC="/jh_cypress_config/userhome"
export JH_CYPRESS_HOME_DEST="/home"

export JH_CYPRESS_USER_PREFIX=""
export JH_CYPRESS_CREATE_USERS="dan"


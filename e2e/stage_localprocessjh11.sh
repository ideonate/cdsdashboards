#!/bin/bash

source stage_localprocess.sh

# Remember very few Docker images work from jupyterhub before 1.2. Only 1.0.0 (needs both zeros)
# https://github.com/jupyterhub/jupyterhub/issues/2852

export JH_CYPRESS_BASE_IMAGE="jupyterhub/jupyterhub:1.1"


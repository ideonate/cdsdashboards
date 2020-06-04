#!/bin/bash


export JH_CYPRESS_SQLITE_SRC="/jh_cypress_config/from.0.0.13.sqlite"

# The DB upgrade is silent, so just check login
# People who attempted to install a fresh 0.0.13 faced this perpetual can't upgrade error. Future versions set them right.
export JH_CYPRESS_TESTS="/e2e/cypress/integration/login.spec.js"


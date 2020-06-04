#!/bin/bash

if [ ! -z "${JH_CYPRESS_JHCONFIG_SRC}" ]; then 
    echo "1 Want to cp from ${JH_CYPRESS_JHCONFIG_SRC} to ${JH_CYPRESS_JHCONFIG_DEST}"
    cp "${JH_CYPRESS_JHCONFIG_SRC}" "${JH_CYPRESS_JHCONFIG_DEST}"
fi

if [ ! -z "${JH_CYPRESS_SQLITE_SRC}" ]; then 
    echo "2 Want to cp from ${JH_CYPRESS_SQLITE_SRC} to ${JH_CYPRESS_SQLITE_DEST}"
    cp "${JH_CYPRESS_SQLITE_SRC}" "${JH_CYPRESS_SQLITE_DEST}"
fi

echo "STARTUP SCRIPT"
echo "$@"

exec "$@"

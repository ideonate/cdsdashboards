#!/bin/bash

echo "STARTUP SCRIPT"


if [ ! -z "${JH_CYPRESS_JHCONFIG_SRC}" ]; then 
    echo "1 Want to cp from ${JH_CYPRESS_JHCONFIG_SRC} to ${JH_CYPRESS_JHCONFIG_DEST}"
    cp "${JH_CYPRESS_JHCONFIG_SRC}" "${JH_CYPRESS_JHCONFIG_DEST}"
fi

if [ ! -z "${JH_CYPRESS_SQLITE_SRC}" ]; then 
    echo "2 Want to cp from ${JH_CYPRESS_SQLITE_SRC} to ${JH_CYPRESS_SQLITE_DEST}"
    cp "${JH_CYPRESS_SQLITE_SRC}" "${JH_CYPRESS_SQLITE_DEST}"
fi

if [ ! -z "${JH_CYPRESS_HOME_SRC}" ]; then 
    echo "3 Want to cp from ${JH_CYPRESS_HOME_SRC} to ${JH_CYPRESS_HOME_DEST}"
    mkdir "${JH_CYPRESS_HOME_DEST}"
    cp -rf ${JH_CYPRESS_HOME_SRC} ${JH_CYPRESS_HOME_DEST}
fi

if [ ! -z "${JH_CYPRESS_CREATE_USERS}" ]; then 
    echo "4 Create users ${JH_CYPRESS_CREATE_USERS}"
    for user in ${JH_CYPRESS_CREATE_USERS}
    do
        echo "Create ${user}"
        useradd $user
    done

fi

echo "$@"

exec "$@"

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

if [ ! -z "${JH_CYPRESS_CREATE_USERS}" ]; then 
    echo "3 Create users ${JH_CYPRESS_CREATE_USERS}"
    for user in ${JH_CYPRESS_CREATE_USERS}
    do
        echo "Create ${JH_CYPRESS_USER_PREFIX}${user}"
        useradd --create-home ${JH_CYPRESS_USER_PREFIX}$user
        chmod o-rwx /home/${JH_CYPRESS_USER_PREFIX}${user}
    done

fi

if [ ! -z "${JH_CYPRESS_HOME_SRC}" ]; then 
    echo "4 Want to cp from ${JH_CYPRESS_HOME_SRC} to ${JH_CYPRESS_HOME_DEST}"
    mkdir ${JH_CYPRESS_HOME_DEST}

    for user in ${JH_CYPRESS_CREATE_USERS}
    do
        echo "Try for ${user}"
        cp -rf ${JH_CYPRESS_HOME_SRC}/${user}/* ${JH_CYPRESS_HOME_DEST}/${JH_CYPRESS_USER_PREFIX}${user}

        echo "Try chown ${JH_CYPRESS_USER_PREFIX}${user} for ${JH_CYPRESS_HOME_DEST}/${JH_CYPRESS_USER_PREFIX}${user}"
        chown -R ${JH_CYPRESS_USER_PREFIX}${user} ${JH_CYPRESS_HOME_DEST}/${JH_CYPRESS_USER_PREFIX}${user}
    done
fi

echo "$@"

exec "$@"

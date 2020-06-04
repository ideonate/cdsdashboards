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
        echo "Create ${user}"
        useradd --create-home $user
        chmod o-rwx /home/${user}
    done

fi

if [ ! -z "${JH_CYPRESS_HOME_SRC}" ]; then 
    echo "4 Want to cp from ${JH_CYPRESS_HOME_SRC} to ${JH_CYPRESS_HOME_DEST}"
    mkdir ${JH_CYPRESS_HOME_DEST}
    cp -rf ${JH_CYPRESS_HOME_SRC} ${JH_CYPRESS_HOME_DEST}

    for user in `ls ${JH_CYPRESS_HOME_DEST}`
    do
        echo "Try chown ${user} for ${JH_CYPRESS_HOME_DEST}/${user}"
        chown -R ${user} ${JH_CYPRESS_HOME_DEST}/${user}
    done
fi

echo "$@"

exec "$@"

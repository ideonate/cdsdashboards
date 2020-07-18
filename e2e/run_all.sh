#!/bin/bash

cd "${0%/*}"

./reset_docker.sh

rm -rf ./cypress/videos
rm -rf ./cypress/screenshots

# Exit build script on first failure
set -e

stages="dockerspawner localprocess tljh localprocessjh10"

if [ ! -z "${E2E_STAGES}" ]; then
    stages="${E2E_STAGES}"
fi

echo "STAGES: $stages"


functests="login voila db11upgrade db13upgrade"

if [ ! -z "${E2E_FUNCTESTS}" ]; then
    functests="${E2E_FUNCTESTS}"
fi

echo "FUNCTESTS: $functests"


for stage in $stages
do

    if [ ! -z "`docker image ls -q e2e_cdsdashboards`" ]; then
        docker image rm e2e_cdsdashboards
    fi

    for functest in $functests
    do

        echo ""
        echo "*****"
        echo "Running stage ${stage} with test ${functest}"
        echo "*****"

        source stage_${stage}.sh

        source functest_${functest}.sh

        export JH_CYPRESS_MEDIAFOLDER="${stage}/${functest}"

        docker-compose up --force-recreate --exit-code-from cypress
        docker-compose down

    done


done


echo ""
echo "Any Screenshots of failures:"
echo "----------------------------"
echo ""

if [ -d "./cypress/screenshots/" ]; then
    find ./cypress/screenshots/ -name "*.png"
fi



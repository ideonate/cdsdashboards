#!/bin/bash

./reset_docker.sh

stages="localprocess tljh dockerspawner"

functests="login voila db11upgrade db13upgrade"

for stage in $stages
do

    docker image rm e2e_cdsdashboards

    for functest in $functests
    do

        echo ""
        echo "*****"
        echo "Running stage ${stage} with test ${functest}"
        echo "*****"

        source stage_${stage}.sh

        source functest_${functest}.sh

        export JH_CYPRESS_MEDIAFOLDER="${stage}_${functest}"

        docker-compose up --force-recreate --exit-code-from cypress
        docker-compose down

    done


done


echo ""
echo "Any Screenshots of failures:"
echo "----------------------------"
echo ""

find ./cypress/screenshots/ -name "*.png"


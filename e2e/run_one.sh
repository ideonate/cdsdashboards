#!/bin/bash

stage=$1

functest=$2

echo ""
echo "*****"
echo "Running stage ${stage} with test ${functest}"
echo "*****"

source stage_${stage}.sh

source functest_${functest}.sh

export JH_CYPRESS_MEDIAFOLDER="${stage}/${functest}"

docker-compose up --force-recreate #--exit-code-from cypress
docker-compose down


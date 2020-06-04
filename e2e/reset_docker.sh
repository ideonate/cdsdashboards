#!/bin/bash

docker stop `docker ps -a --filter=label='com.containds.e2etest=container' -q`
docker rm `docker ps -a --filter=label='com.containds.e2etest=container' -q`

docker image rm `docker image ls --filter=label='com.containds.e2etest=image' -q`




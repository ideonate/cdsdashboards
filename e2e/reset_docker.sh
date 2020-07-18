#!/bin/bash

$docker_stop=`docker ps -a --filter=label='com.containds.e2etest=container' -q`
if [ ! -z "$docker_stop" ]; then
    docker stop $docker_stop
    docker rm $docker_rm
fi


$docker_image=`docker image ls --filter=label='com.containds.e2etest=image' -q`

if [ ! -z "$docker_image" ]; then
    docker image rm $docker_image
fi


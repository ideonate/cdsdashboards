#!/bin/bash

cd "${0%/*}"

cd voila-oauth

docker build -t mycompany/jh-voila-oauth-singleuser:singleuser-1.2 .

latest_tag=dc9744740e12
docker build --build-arg BASE_REPO=jupyter/scipy-notebook --build-arg TAG=$latest_tag -t mycompany/jh-voila-oauth-singleuser:scipy-$latest_tag .

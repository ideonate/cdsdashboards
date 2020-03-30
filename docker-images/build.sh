#!/bin/bash

cd "${0%/*}"

cd voila-public

docker build -t ideonate/jh-voila-public-singleuser:1.2 .

cd ../voila-oauth

docker build -t ideonate/jh-voila-oauth-singleuser:1.2 .

latest_tag=dc9744740e12
docker build --build-arg BASE_REPO=jupyter/scipy-notebook --build-arg TAG=$latest_tag -t ideonate/jh-voila-oauth-singleuser:$latest_tag .

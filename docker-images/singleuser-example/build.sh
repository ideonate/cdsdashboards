#!/bin/bash

cd "${0%/*}"

cd containds-all-example

docker build -t containds-all-example --build-arg JHSINGLENATIVEPROXY_LINE=https://github.com/ideonate/jhsingle-native-proxy/archive/0.5.0-b1.zip .

# --build-arg JHSINGLENATIVEPROXY_LINE=https://github.com/ideonate/jhsingle-native-proxy/archive/0.5.0-b1.zip
# --build-arg JHSINGLENATIVEPROXY_LINE=JHSINGLENATIVEPROXY_LINE=jhsingle-native-proxy==0.5.0-b1
# --build-arg BASE_REPO=jupyter/scipy-notebook
# --build-arg TAG=latest
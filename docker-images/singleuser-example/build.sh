#!/bin/bash

cd "${0%/*}"

cd containds-all-example

docker build -t containds-all-example .

# --build-arg JHSINGLENATIVEPROXY_LINE=https://github.com/ideonate/jhsingle-native-proxy/archive/0.4.0-beta.1.zip
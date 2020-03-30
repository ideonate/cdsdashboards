#!/bin/bash

cd "${0%/*}"

cd voila-public

docker build -t ideonate/jh-voila-public-singleuser:1.2 .

cd ../voila-oauth

docker build -t ideonate/jh-voila-oauth-singleuser:1.2 .

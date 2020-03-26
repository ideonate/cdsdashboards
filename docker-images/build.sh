#!/bin/bash

cd "${0%/*}"

docker build -t ideonate/jh-voila-singleuser:1.2 .

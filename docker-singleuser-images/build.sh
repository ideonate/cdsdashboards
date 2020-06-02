#!/bin/bash

cd "${0%/*}"

cd containds-all-example

docker build -t containds-all-example .


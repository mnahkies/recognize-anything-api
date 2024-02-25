#!/usr/bin/env bash

set -exo pipefail

./bin/docker-build.sh

docker tag recognize-anything-api mnahkies/recognize-anything-api:latest
docker push mnahkies/recognize-anything-api:latest

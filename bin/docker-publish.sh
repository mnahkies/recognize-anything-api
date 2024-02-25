#!/usr/bin/env bash

set -exo pipefail

./bin/docker-build.sh

TAG=$(python setup.py --version)

docker tag recognize-anything-api mnahkies/recognize-anything-api:latest
docker tag recognize-anything-api "mnahkies/recognize-anything-api:$TAG"

docker push mnahkies/recognize-anything-api:latest
docker push "mnahkies/recognize-anything-api:$TAG"

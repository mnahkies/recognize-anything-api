#!/usr/bin/env bash

set -exo pipefail

docker run -it --rm \
    --gpus all \
    -e MODEL_NAME=ram_plus \
    -p 8000:8000 \
    recognize-anything-api

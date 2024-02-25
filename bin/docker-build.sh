#!/usr/bin/env bash

set -exo pipefail

docker build \
  --progress=plain \
  --label org.opencontainers.image.source="$(git remote get-url origin)" \
  --label org.opencontainers.image.revision="$(git rev-parse HEAD)" \
  --label org.opencontainers.image.version="$(python setup.py --version)" \
  -t recognize-anything-api .

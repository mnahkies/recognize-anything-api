#!/usr/bin/env bash

set -exo pipefail

docker build --progress=plain -t recognize-anything-api .

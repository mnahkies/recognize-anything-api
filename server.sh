#!/usr/bin/env bash

set -eo pipefail

python3 -m uvicorn --host=0.0.0.0 --port=8000 server:app

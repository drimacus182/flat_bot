#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
cd ${SCRIPT_DIR}

echo `date` >> log.txt
env/bin/python3 bot.py >> log.txt 2>&1

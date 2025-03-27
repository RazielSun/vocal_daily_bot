#!/bin/bash

# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail
IFS=$'\n\t'

pip install -r requirements.txt

python ./scripts/translate.py --compile

echo "Deploy completed!"
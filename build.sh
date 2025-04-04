#!/bin/bash

# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail
IFS=$'\n\t'

python ./scripts/translation.py --compile
python ./scripts/update_content.py --csv

echo "✅ Build complete"
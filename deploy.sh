#!/bin/bash

# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail
IFS=$'\n\t'

# pip install -r requirements.txt

python ./scripts/translation.py --compile
python ./scripts/update_content.py --csv
echo "Preparation completed!"

echo "🚀 Starting bot"
python -m bot
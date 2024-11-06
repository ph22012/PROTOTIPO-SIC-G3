#!/usr/bin/env bash

set -o errexit

pip install -r requirements.txt

python manage.py collecStatic --noimnut
python manage.py migrate
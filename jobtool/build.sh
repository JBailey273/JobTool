#!/usr/bin/env bash
set -o errexit

python -m pip install --upgrade pip
pip install -r requirements.txt

# Django static + DB setup
python manage.py collectstatic --noinput
python manage.py migrate --noinput --run-syncdb

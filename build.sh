#!/usr/bin/env bash
set -o errexit
set -o pipefail
set -o nounset


python -V
python -m pip install --upgrade pip
python -m pip install --no-cache-dir -r requirements.txt


# Run migrations before collectstatic so DB is ready
python manage.py migrate --noinput --run-syncdb
python manage.py collectstatic --noinput

#!/bin/bash
set -euo pipefail

cd /var/www/blackbook.sc.tz

git fetch origin main
git reset --hard origin/main

./venv/bin/pip install -q -r requirements.txt
./venv/bin/python manage.py migrate --noinput
./venv/bin/python manage.py collectstatic --noinput

systemctl restart gunicorn-thesystem

echo "Deploy finished: $(date -u '+%Y-%m-%d %H:%M:%S UTC') — $(git rev-parse --short HEAD)"

#!/bin/sh
cd ${DJANGO_ROOT}
npm install
python manage.py migrate
pysassc --sourcemap -I node_modules scss/site.scss static/site/css/site.css
python manage.py sitetree_resync_apps
python manage.py collectstatic --noinput
python icon_import.py
# exec uvnicorn ${APP_NAME}.wsgi:application --host 0.0.0.0 --port 8000 --workers 5 --access-log --use-colors
exec gunicorn ${APP_NAME}.wsgi:application --bind 0.0.0.0:8000 --worker-connections 5 --access-logfile /dev/stdout --error-logfile /dev/stdout

#!/bin/sh
while true; do
    flask db upgrade
    if [ $? -eq 0 ]; then
        break
    fi
    echo Upgrade command failed, retrying in 5 secs...
    sleep 5
done
flask create-superuser
flask download-proxies
flask cache-useragent

exec celery worker -A app.celery -c 8 --logfile - &
exec flower -A app.celery &
exec gunicorn -b :5000 --access-logfile - --error-logfile - thumbsup:app

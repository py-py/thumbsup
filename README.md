### Make environment
```
python3 -m venv venv/
pip install -r requirements.txt
```

### Clone project
```
git clone https://github.com/py-py/thumbsup.git
```

### Start background app
```
cd thumbsup
docker-compose up -d
```

### Local development
Run services:
- redis
- mysql

Run application:
```
cd thumbsup
flask create-superuser
flask download-proxies
flask cache-useragent
celery worker -A app.celery -c 8 --logfile - &
celery beat -A app.celery --logfile - &
flower -A app.celery &
flask run
```

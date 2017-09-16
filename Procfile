web: gunicorn riskproject.wsgi --log-file -
worker: celery -A riskproject worker
beat: celery -A riskproject beat -S django
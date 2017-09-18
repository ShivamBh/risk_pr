web: gunicorn riskproject.wsgi --log-file -
worker: celery -A riskproject worker --loglevel=DEBUG
beat: celery -A riskproject beat -S django --loglevel=DEBUG
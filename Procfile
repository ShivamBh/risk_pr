web: gunicorn riskproject.wsgi --log-file -
worker: celery -A riskproject worker --loglevel=INFO
beat: celery -A riskproject beat -S django --loglevel=INFO
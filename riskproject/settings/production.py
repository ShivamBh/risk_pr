from __future__ import absolute_import, unicode_literals
import dj_database_url


from .base import *
DEBUG = True
SECRET_KEY = '8w@+-dis^dpj-e35xb1twx*#gg%l^nrvv+d&ijlz72^&k_j%-r'
TWILIO_ACCOUNT_SID = 'AC2ba82ee6202e458e2b821999d28642e0'
TWILIO_AUTH_TOKEN = '7ddd22bd03373e05e5cbc49a7087bb7f'
TWILIO_PHONE_NUMBER = '+14159149102'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'ShivamBh'
EMAIL_HOST_PASSWORD = 'sendgrid99*&'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'info@issrisk.com'
SERVER_EMAIL = 'info@issrisk.com'

ALLOWED_HOSTS = ['localhost', 'issdemo.herokuapp.com']

db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env) 

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

try:
    from .local import *
except ImportError:
    pass

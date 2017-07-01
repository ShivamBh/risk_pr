from __future__ import absolute_import, unicode_literals
import dj_database_url


from .base import *
DEBUG = True


ALLOWED_HOSTS = ['localhost', 'issdemo.herokuapp.com']

db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env) 

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

try:
    from .local import *
except ImportError:
    pass

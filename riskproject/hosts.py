
from django_hosts import patterns, host
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings 
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

host_patterns = patterns('',
	host(r'intel', settings.ROOT_URLCONF, name='intel'),
	host(r'intel', 'reports.urls', name='iss_home'),
	host(r'cms', 'cms.urls', name='iss_cms'),
)

host_patterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
host_patterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
host_patterns += staticfiles_urlpatterns()
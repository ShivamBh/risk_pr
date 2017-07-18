from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns('',
	host(r'intel', settings.ROOT_URLCONF, name='intel'),
	host(r'intel', 'reports.urls', name='iss_home'),
	host(r'cms', 'cms.urls', name='iss_cms'),
)
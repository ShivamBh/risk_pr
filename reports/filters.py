from django.contrib.auth.models import User

from accounts.models import Profile
from .models import Report, Country

import django_filters

class UserFilter(django_filters.FilterSet):
	class Meta:
		model = Report
		fields = ['location', 'title', 'report_type']

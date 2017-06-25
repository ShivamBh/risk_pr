from django.conf.urls import url
from .views import ReportListView, CountryListView

urlpatterns = [
	#url(r'^$', index, name='home'),
	url(r'^$', ReportListView.as_view(), name='report_list'),
	url(r'^country/$', CountryListView.as_view(), name='country_list'),
]
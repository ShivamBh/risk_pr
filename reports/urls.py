from django.conf.urls import url
from .views import ReportListView, CountryListView, ReportDetailView, CountryDetailView, index

urlpatterns = [
	url(r'^$', index, name='home'),
	url(r'^reports/$', ReportListView.as_view(), name='report_list'),
	url(r'^country/$', CountryListView.as_view(), name='country_list'),
	url(r'^country/(?P<pk>[0-9]+)/detail/$', CountryDetailView.as_view(), name='country_detail'),
	url(r'^report/(?P<pk>[0-9]+)/detail/$', ReportDetailView.as_view(), name='report_detail'),

]
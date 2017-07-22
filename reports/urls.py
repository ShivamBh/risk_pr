from django.conf.urls import url
from .views import ReportListView, CountryListView, ReportDetailView, CountryDetailView, index

urlpatterns = [
	url(r'^$', index, name='home'),
	url(r'^reports/$', ReportListView.as_view(), name='report_list'),
	url(r'^country/$', CountryListView.as_view(), name='country_list'),
	url(r'^country/(?P<pk>[0-9]+)/detail/$', CountryDetailView.as_view(), name='country_detail'),
	url(r'^report/(?P<pk>[0-9]+)/detail/$', ReportDetailView.as_view(), name='report_detail'),
	# url(r'^account_activation_sent/$', account_activation_sent, name='account_activation_sent_client'),
	# url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate_client'),
]
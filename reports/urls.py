from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings 
from django.conf.urls.static import static
from django.conf.urls import url, include
from .views import user_profile_view, user_profile_edit, change_password, SearchListView , ReportListView, CountryListView, ReportDetailView, CountryDetailView, index

urlpatterns = [
	url(r'^$', index, name='home'),
	url(r'^change-password/$', change_password, name='change_password_intel'),
	url(r'^reports/$', ReportListView.as_view(), name='report_list'),
	url(r'^search/$', SearchListView.as_view(), name='report_search'),
	url(r'^country/$', CountryListView.as_view(), name='country_list'),
	url(r'^profile/$', user_profile_view, name='user_profile'),
	url(r'^edit-profile/$', user_profile_edit, name='user_profile_edit'),
	url(r'^country/(?P<pk>[0-9]+)/detail/$', CountryDetailView.as_view(), name='country_detail'),
	url(r'^report/(?P<pk>[0-9]+)/detail/$', ReportDetailView.as_view(), name='report_detail'),
	# url(r'^account_activation_sent/$', account_activation_sent, name='account_activation_sent_client'),
	# url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate_client'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
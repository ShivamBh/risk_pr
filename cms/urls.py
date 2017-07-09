from django.conf.urls import url
from .views import ReportListView, CountryDetailView, CountryListView, FlashMessageCreateView, cms_home_view, create_user_view,  update_user_view,  CreateReportView, UpdateReportView, DeleteReportView, CreateCountryView, UpdateCountryView, DeleteCountryView

urlpatterns = [
	url(r'^$', cms_home_view, name='cms_home'),
	url(r'^create-flash/$', FlashMessageCreateView.as_view(), name='create_flash'),
	url(r'^create-user/$', create_user_view, name='create_user'),
	url(r'^update-user/(?P<id>[\d]+)/$', update_user_view, name='update_user'),
	url(r'^reports/$', ReportListView.as_view(), name='report_list_cms'),
	url(r'^create-report/$', CreateReportView.as_view(), name='create_report'),
	url(r'^update-report/(?P<pk>[\d]+)/$', UpdateReportView.as_view(), name='update_report'),
	url(r'^delete-report/(?P<pk>[\d]+)/$', DeleteReportView.as_view(), name='delete_report'),
	url(r'^countries/$', CountryListView.as_view(), name='country_list_cms'),
	url(r'^create-country/$', CreateCountryView.as_view(), name='create_country'),
	url(r'^update-country/(?P<pk>[\d]+)/$', UpdateCountryView.as_view(), name='update_country'),
	url(r'^delete-country/(?P<pk>[\d]+)/$', DeleteCountryView.as_view(), name='delete_country'),
	url(r'^country-detail/(?P<pk>[\d]+)/$', CountryDetailView.as_view(), name='country_detail_cms'),

]
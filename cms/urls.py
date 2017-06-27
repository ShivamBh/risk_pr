from django.conf.urls import url
from .views import cms_home_view, CreateReportView, UpdateReportView, DeleteReportView, CreateCountryView, UpdateCountryView, DeleteCountryView

urlpatterns = [
	url(r'^$', cms_home_view, name='cms_home'),
	url(r'^create-report/$', CreateReportView.as_view(), name='create_report'),
	url(r'^update-report/(?P<pk>[\d]+)/$', UpdateReportView.as_view(), name='update_report'),
	url(r'^delete-report/(?P<pk>[\d]+)/$', DeleteReportView.as_view(), name='delete_report'),
	url(r'^create-country/$', CreateCountryView.as_view(), name='create_country'),
	url(r'^update-country/(?P<pk>[\d]+)/$', UpdateCountryView.as_view(), name='update_country'),
	url(r'^delete-country/(?P<pk>[\d]+)/$', DeleteCountryView.as_view(), name='delete_country'),

]
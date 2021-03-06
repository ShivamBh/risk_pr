from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings 
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import change_password, user_list_view, user_detail_view, activate ,account_activation_sent, DeleteUserView, ReportListView, ReportDetailView, CountryDetailView, CountryListView, cms_home_view, create_user_view,  update_user_view,  CreateReportView, UpdateReportView, DeleteReportView, CreateCountryView, UpdateCountryView, DeleteCountryView

urlpatterns = [
	url(r'^$', cms_home_view, name='cms_home'),
	url(r'^login/$', auth_views.login, name='login'),
	url(r'^logout/$', auth_views.logout, name='logout'),
	# url('^', include('django.contrib.auth.urls')),
	url(r'^admin/', admin.site.urls),
	url(r'^account_activation_sent/$', account_activation_sent, name='account_activation_sent_staff'),
	url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate_staff'),
    url(r'^change-password/$', change_password, name='change_password_cms'),
    # url(r'^password-reset/$', auth_views.password_reset, name='password_reset'),
    # url(r'^password-reset/done/$', auth_views.password_reset_done,  name='password_reset_done'),
    # url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    # url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^user-list/$', user_list_view, name='user_list'),
	url(r'^create-user/$', create_user_view, name='create_user'),
	url(r'^update-user/(?P<id>[\d]+)/$', update_user_view, name='update_user'),
	url(r'^user-detail/(?P<id>[\d]+)/$', user_detail_view, name='user_detail'),
	url(r'^delete-user/(?P<pk>[\d]+)/$', DeleteUserView.as_view(), name='delete_user'),
	url(r'^reports/$', ReportListView.as_view(), name='report_list_cms'),
	url(r'^report-detail/(?P<pk>[\d]+)/$', ReportDetailView.as_view(), name='report_detail_cms'),
	url(r'^create-report/$', CreateReportView.as_view(), name='create_report'),
	url(r'^update-report/(?P<pk>[\d]+)/$', UpdateReportView.as_view(), name='update_report'),
	url(r'^delete-report/(?P<pk>[\d]+)/$', DeleteReportView.as_view(), name='delete_report'),
	url(r'^countries/$', CountryListView.as_view(), name='country_list_cms'),
	url(r'^create-country/$', CreateCountryView.as_view(), name='create_country'),
	url(r'^update-country/(?P<pk>[\d]+)/$', UpdateCountryView.as_view(), name='update_country'),
	url(r'^delete-country/(?P<pk>[\d]+)/$', DeleteCountryView.as_view(), name='delete_country'),
	url(r'^country-detail/(?P<pk>[\d]+)/$', CountryDetailView.as_view(), name='country_detail_cms'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
from django.conf.urls import url
from .views import CreateReportView

urlpatterns = [
	url(r'^create-report/$', CreateReportView.as_view(), name='create_report'),
]
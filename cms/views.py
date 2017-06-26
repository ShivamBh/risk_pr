from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import ReportForm
from reports.models import Report, Country

# Create your views here.
class CreateReportView(CreateView):
	model = Report
	template_name = 'cms/create_report.html'
	form_class = ReportForm
	
	success_url = '/reports/'

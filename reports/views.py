from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Report, Country

# Create your views here.
class ReportListView(ListView):
	model = Report
	context_object_name = 'report_list'
	template_name = 'reports/report_list.html'

class CountryListView(ListView):
	model = Country
	context_object_name = 'country_list'
	template_name = 'reports/country_list.html'
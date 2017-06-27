from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

from .models import Report, Country

# Create your views here.
@login_required
def index(request):
	return render(request, 'reports/index.html')

class ReportListView(LoginRequiredMixin, ListView):
	model = Report
	#queryset = Report.objects.filter('-created_at')
	context_object_name = 'report_list'
	template_name = 'reports/report_list.html'

class CountryListView(LoginRequiredMixin, ListView):
	model = Country
	context_object_name = 'country_list'
	template_name = 'reports/country_list.html'

class ReportDetailView(LoginRequiredMixin, DetailView):
	model = Report
	slug_field = 'pk'
	context_object_name = 'report'
	template_name = 'reports/report_detail.html'

class CountryDetailView(LoginRequiredMixin, DetailView):
	model = Country
	slug_field = 'pk'
	context_object_name = 'country'
	template_name = 'reports/country_detail.html'
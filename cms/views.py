from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import ReportForm, CountryForm
from reports.models import Report, Country

# Create your views here.
def cms_home_view(request):
	reports = Report.objects.all()
	countries = Country.objects.all()
	template = 'cms/cms_home.html'
	return render(request, template, {'reports': reports, 'countries':countries})

class CreateReportView(CreateView):
	model = Report
	template_name = 'cms/create_report.html'
	form_class = ReportForm
	
	success_url = '/cms/'

class UpdateReportView(UpdateView):
	model = Report
	slug_field='pk'
	template_name = 'cms/update_report.html'
	form_class = ReportForm
	success_url = '/cms/'

class DeleteReportView(DeleteView):
	model = Report
	slug_field = 'pk'
	template_name = 'cms/delete_report.html'
	success_url = '/cms/'

class CreateCountryView(CreateView):
	model = Country
	template_name = 'cms/create_country.html'
	form_class = CountryForm
	success_url = '/cms/'

class UpdateCountryView(UpdateView):
	model = Country
	slug_field = 'pk'
	template_name = 'cms/update_country.html'
	form_class = CountryForm
	success_url = '/cms/'

class DeleteCountryView(DeleteView):
	model = Country
	slug_field = 'pk'
	template_name = 'cms/delete_country.html'
	success_url = '/cms/'

from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from accounts.models import Profile
from .models import Report, Country

# Create your views here.
@login_required
def index(request):
	user = request.user
	qs = Profile.objects.get(user=user)
	loc = qs.sub_country.all()
	rep_qs = [(Report.objects.filter(location__name__icontains=loc_obj.name)) for loc_obj in loc]
	reports = [item for sublist in rep_qs for item in sublist]

	return render(request, 'reports/index.html', {'loc':loc, 'rep_qs': reports})

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
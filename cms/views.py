from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
from .forms import ReportForm, CountryForm, ProfileForm, UserForm
from reports.models import Report, Country
from accounts.models import Profile 

# Create your views here.
def cms_home_view(request):
	reports = Report.objects.all()
	countries = Country.objects.all()
	user_list = User.objects.all()
	template = 'cms/cms_home.html'
	return render(request, template, {'reports': reports, 'countries':countries, 'users': user_list})

def update_user_view(request, id):
	instance_obj = get_object_or_404(User, pk=id)
	if request.method == 'POST':
		user_form = UserForm(request.POST, instance=instance_obj)
		profile_form = ProfileForm(request.POST, instance=instance_obj.profile)

		if all([user_form.is_valid(), profile_form.is_valid()]):
			user = user_form.save()
			profile = profile_form.save()
			return render(request, 'cms/cms_home.html')
	else:
		user_form = UserForm(instance = instance_obj)
		profile_form = ProfileForm(instance = instance_obj.profile)

	return render(request, 'cms/update_user.html', {'user_form': user_form, 'profile_form': profile_form})


# class UpdateUserView(UpdateView):
# 	model = Profile
# 	fields = ['phone_number', 'company', 'sub_country', 'sub_model']
# 	template_name = 'cms/update_user.html'
# 	slug_field = 'pk'
# 	#slug_url_kwarg = 'slug'


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

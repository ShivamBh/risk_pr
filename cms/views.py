from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User, Permission, Group
from django.contrib.auth.forms import UserCreationForm

from .forms import ReportForm, CountryForm, ProfileForm, UserForm, UserCreateForm, ProfileCreateForm, CMSLoginForm
from reports.models import Report, Country
from accounts.models import Profile 

# Create your views here
@login_required
def cms_home_view(request):
	reports = Report.objects.all()
	countries = Country.objects.all()
	perm = Group.objects.all()
	user_list = User.objects.all()
	template = 'cms/cms_home.html'
	return render(request, template, {'reports': reports, 'countries':countries, 'users': user_list, 'perm': perm})

# def cms_login(request):
# 	if request.method == 'POST':
# 		login_form = CMSLoginForm(request.POST)

# 		if login_form.is_valid():
# 			cd = form.cleaned_data
# 			user = authenticate(username=cd['username'], password=cd['password'])

# 			if user is not None:
# 				if user.is_active:
# 					login(request, user)
# 					return redirect('cms_home')
# 				else:
# 					return HttpResponse('Disabled Account')
# 			else:
# 				return 



@login_required
@permission_required('auth.change_user', login_url='/login/')
def update_user_view(request, id):
	instance_obj = get_object_or_404(User, pk=id)
	if request.method == 'POST':
		user_form = UserForm(request.POST, instance=instance_obj)
		profile_form = ProfileForm(request.POST, instance=instance_obj.profile)

		if all([user_form.is_valid(), profile_form.is_valid()]):
			user = user_form.save()
			profile = profile_form.save()
			#implement messages (messages framework)
			return redirect('cms_home')
	else:
		user_form = UserForm(instance = instance_obj)
		profile_form = ProfileForm(instance = instance_obj.profile)

	return render(request, 'cms/update_user.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
@permission_required('auth.add_user', login_url='/login/')
def create_user_view(request):
	mod = Group.objects.get(name='moderators')
	pub = Group.objects.get(name='publishers')
	if request.method == 'POST':
		user_form = UserCreateForm(request.POST)
		profile_form = ProfileCreateForm(request.POST)

		if all([user_form.is_valid(), profile_form.is_valid()]):
			user = user_form.save()
			user.refresh_from_db
			user.profile.phone_number = profile_form.cleaned_data.get('phone_number')
			user.profile.company = profile_form.cleaned_data.get('company')
			user.profile.sub_country = profile_form.cleaned_data.get('sub_country')
			user.profile.sub_model = profile_form.cleaned_data.get('sub_model')
			user.profile.is_moderator = profile_form.cleaned_data.get('is_moderator')
			user.profile.is_publisher = profile_form.cleaned_data.get('is_publisher')
			if user.profile.is_moderator:
				mod.user_set.add(user)
				user.save()
				return redirect('cms_home')
			elif user.profile.is_publisher:
				pub.user_set.add(user)
				user.save()
				return redirect('cms_home')
			else:
				user.save()
				return redirect('cms_home')
	else:
		user_form = UserCreateForm()
		profile_form = ProfileCreateForm()

	return render(request, 'cms/create_user.html', {'user_form':user_form, 'profile_form':profile_form})


# class UpdateUserView(UpdateView):
# 	model = Profile
# 	fields = ['phone_number', 'company', 'sub_country', 'sub_model']
# 	template_name = 'cms/update_user.html'
# 	slug_field = 'pk'
# 	#slug_url_kwarg = 'slug'


class CreateReportView(PermissionRequiredMixin, CreateView):
	permission_required = ('reports.add_report')
	model = Report
	template_name = 'cms/create_report.html'
	form_class = ReportForm
	
	success_url = '/cms/'

class UpdateReportView(PermissionRequiredMixin, UpdateView):
	permission_required = ('reports.change_report')
	model = Report
	slug_field='pk'
	template_name = 'cms/update_report.html'
	form_class = ReportForm
	success_url = '/cms/'

class DeleteReportView(PermissionRequiredMixin, DeleteView):
	permission_required = ('reports.delete_report')
	model = Report
	slug_field = 'pk'
	template_name = 'cms/delete_report.html'
	success_url = '/cms/'

class CreateCountryView(PermissionRequiredMixin, CreateView):
	permission_required = ('reports.add_country')
	model = Country
	template_name = 'cms/create_country.html'
	form_class = CountryForm
	success_url = '/cms/'

class UpdateCountryView(PermissionRequiredMixin, UpdateView):
	permission_required = ('reports.change_country')
	model = Country
	slug_field = 'pk'
	template_name = 'cms/update_country.html'
	form_class = CountryForm
	success_url = '/cms/'

class DeleteCountryView(PermissionRequiredMixin, DeleteView):
	permission_required = ('reports.delete_country')
	model = Country
	slug_field = 'pk'
	template_name = 'cms/delete_country.html'
	success_url = '/cms/'
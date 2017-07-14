from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User, Permission, Group
from django.contrib.auth.forms import UserCreationForm
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from riskproject.settings import DEFAULT_FROM_EMAIL

from .forms import ReportForm, FlashMessageForm, ReportUpdateForm,  CountryForm, ProfileForm, UserForm, UserCreateForm, ProfileCreateForm, CMSLoginForm
from reports.models import Report, Country
from accounts.models import Profile 
from .models import FlashMessage
from .utils import send_twilio_message
from .tokens import account_activation_token

# Create your views here
@login_required
@permission_required('reports.add_report', login_url='/login/')
def cms_home_view(request):
	reports = Report.objects.all().order_by('-created_at')
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

# @login_required
# @permission_required('auth.change_user', login_url='/login/')
# def user_list_view(request):
# 	template = 'cms/user_list.html'
# 	user_list = User.objects.all()
# 	reg_users = Profile.objects.filter(Q(is_moderator=False) & Q(is_publisher=False))


@login_required
@permission_required('auth.change_user', login_url='/login/')
def update_user_view(request, id):
	mod = Group.objects.get(name='moderators')
	pub = Group.objects.get(name='publishers')
	instance_obj = get_object_or_404(User, pk=id)
	if request.method == 'POST':
		user_form = UserForm(request.POST, instance=instance_obj)
		profile_form = ProfileCreateForm(request.POST, instance=instance_obj.profile)

		if all([user_form.is_valid(), profile_form.is_valid()]):
			user = user_form.save()
			profile = profile_form.save()
			# user = user_form.save()
			# user.refresh_from_db
			# user.profile.phone_number = profile_form.cleaned_data.get('phone_number')
			# user.profile.company = profile_form.cleaned_data.get('company')
			# user.profile.sub_country = profile_form.cleaned_data.get('sub_country')
			# user.profile.sub_model = profile_form.cleaned_data.get('sub_model')
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
			#implement messages (messages framework)
			# return redirect('cms_home')
	else:
		user_form = UserForm(instance = instance_obj)
		profile_form = ProfileCreateForm(instance = instance_obj.profile)

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

			# user_form.fields['is_moderator'].widget.attrs['disabled'] = True

			user.profile.is_moderator = profile_form.cleaned_data.get('is_moderator')
			user.profile.is_publisher = profile_form.cleaned_data.get('is_publisher')
			
			#Signup email, with activation link
			
			user.save()
			current_site = get_current_site(request)
			subject = 'Set custom password - ISSRisk'
			message = render_to_string('cms/account_activation_email.html', {
				'user': user,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': account_activation_token.make_token(user),

			})
			send_mail(subject, message, DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)

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


class ReportListView(PermissionRequiredMixin, ListView):
	permission_required = ('reports.add_report')
	model = Report
	template_name = 'cms/report_list.html'
	context_object_name = 'report_list'



class CreateReportView(PermissionRequiredMixin, CreateView):
	permission_required = ('reports.add_report')
	model = Report
	template_name = 'cms/create_report.html'
	form_class = ReportForm
	
	success_url = '/cms/'

	def form_valid(self, form):
		title = form.cleaned_data['title']
		send_mail('test', title, 'helpdesk@info.issrisk.com', ['shivam.bhattacharjee94@gmail.com'])
		return super(CreateReportView, self).form_valid(form)

class UpdateReportView(PermissionRequiredMixin, UpdateView):
	permission_required = ('reports.change_report')
	model = Report
	slug_field='pk'
	template_name = 'cms/update_report.html'
	form_class = ReportUpdateForm
	success_url = '/cms/'

	# def form_valid(self, form):

	# 	is_major = form.cleaned_data['major_revision']
	# 	loc = form.cleaned_data['location']
		
	# 	queryset = Profile.objects.filter(sub_country__name__icontains=loc)
	# 	if is_major:
	# 		#send batch email

class DeleteReportView(PermissionRequiredMixin, DeleteView):
	permission_required = ('reports.delete_report')
	model = Report
	slug_field = 'pk'
	template_name = 'cms/delete_report.html'
	success_url = '/cms/'

class CountryListView(PermissionRequiredMixin, ListView):
	permission_required = ('reports.add_report')
	model = Country
	template_name = 'cms/country_list.html'
	context_object_name = 'country_list'

class CountryDetailView(PermissionRequiredMixin, DetailView):
	permission_required = ('reports.add_report')
	model = Country
	slug_field = 'pk'
	context_object_name = 'country'
	template_name = 'cms/country_detail.html'

	def get_context_data(self, **kwargs):
		context = super(CountryDetailView, self).get_context_data(**kwargs)
		# ct = Country.objects.get(pk=slug_field)
		rel_reps = Report.objects.filter(location__name__icontains=self.object.name).order_by('-created_at')
		context["rel_reps"] = rel_reps
		return context

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


class FlashMessageCreateView(PermissionRequiredMixin, CreateView):
	permission_required = ('reports.add_country')
	model = FlashMessage
	template_name = 'cms/create_flash.html'
	form_class = FlashMessageForm
	success_url = '/cms/'

	def form_valid(self, form):
		def get_recipient_list(qs):
			arr = []
			

		body = form.cleaned_data['body']
		loc = form.cleaned_data['location']
		queryset = Profile.objects.filter(sub_country__name__icontains=loc)

		#send batch sms
		for item in queryset:
			if item.phone_number == "":
				continue
			else:
				send_twilio_message(item.phone_number, body)

		# rec_arr = get_recipient_list(queryset)
		# sent = 

		send_sms = form.save()


		return super(FlashMessageCreateView, self).form_valid(form)
	



		
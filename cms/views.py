from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.core import mail
from django.core.mail import send_mail, send_mass_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User, Permission, Group
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import Context
from django.template.loader import render_to_string, get_template
# from django.urls import reverse
from django_hosts.resolvers import reverse
from riskproject.settings import DEFAULT_FROM_EMAIL
import logging
import pdb

from pyshorteners import Shortener

from .forms import ReportForm, ReportUpdateForm,  CountryForm, ProfileForm, UserForm, UserCreateForm, ProfileCreateForm, CMSLoginForm
from reports.models import Report, Country
from accounts.models import Profile 
from .utils import send_twilio_message
from .tokens import account_activation_token

# Create your views here

# def cms_login(request):
# 	return HttpResponse('login page cms')


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
def user_list_view(request):
	template = 'cms/user_list.html'
	user_list = User.objects.all()
	active_users = User.objects.filter(is_active=True).exclude(is_staff=True)
	staff_users = User.objects.filter(is_staff=True)
	inactive_users = User.objects.filter(is_active=False)

	context = {
		'active_users': active_users,
		'staff_users': staff_users,
		'inactive_users': inactive_users,
	}
	return render(request, template, context)

@login_required
@permission_required('auth.change_user', login_url='/login/')
def update_user_view(request, id):
	mod = Group.objects.get(name='moderators')
	pub = Group.objects.get(name='publishers')
	instance_obj = get_object_or_404(User, pk=id)
	if request.method == 'POST':
		user_form = UserForm(request.POST, instance=instance_obj)
		profile_form = ProfileForm(request.POST, instance=instance_obj.profile)

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
		profile_form = ProfileForm(instance = instance_obj.profile)

	return render(request, 'cms/update_user.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
@permission_required('auth.add_user', login_url='/login/')
def create_user_view(request):
	logger = logging.getLogger(__name__)
	# try:
	# 	profile_object = request.user.profile
	# except Profile.DoesNotExist:
	# 	profile_object = Profile(user=request.user)
	mod = Group.objects.get(name='moderators')
	pub = Group.objects.get(name='publishers')
	
	if request.method == 'POST':
		user_form = UserCreateForm(request.POST)
		profile_form = ProfileCreateForm(data=request.POST)
		#print("first point")
		if all([user_form.is_valid(), profile_form.is_valid()]):
			#print("after if is_valid")
			user = user_form.save()
			user.refresh_from_db
			user.profile.phone_number = profile_form.cleaned_data.get('phone_number')
			user.profile.company = profile_form.cleaned_data.get('company')
			user.profile.sub_country = profile_form.cleaned_data.get('sub_country')
			user.profile.sub_model = profile_form.cleaned_data.get('sub_model')
			##print("after profile clean")
			new_password = User.objects.make_random_password()
			user.set_password(new_password)
			# profile.user = user
			# profile.save()
			# user_form.fields['is_moderator'].widget.attrs['disabled'] = True
		
			user.profile.is_moderator = profile_form.cleaned_data.get('is_moderator')
			user.profile.is_publisher = profile_form.cleaned_data.get('is_publisher')
			
			#Signup email, with activation link
			#print("before save")
			user.save()
			user.profile.save()
			#print("after save")
			current_site = get_current_site(request)
			subject = 'Account Activation - ISSRISK'

			message = render_to_string('cms/account_activation_email.html' , {
				'user': user,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': account_activation_token.make_token(user),
				'password': new_password,
			})

			user.email_user(subject, message)
			# print(user)
			# print(user.profile)
			if user.profile.is_moderator:
				#print("after email1")
				mod.user_set.add(user)
				user.save()
				user.profile.save()
				return redirect('account_activation_sent_staff')
			elif user.profile.is_publisher:
				#print("after email2")
				pub.user_set.add(user)
				user.save()
				user.profile.save()
				return redirect('account_activation_sent_staff')
			else:
				#print("after email3")
				user.save()
				user.profile.save()
				return redirect('account_activation_sent_staff')

	else:
		user_form = UserCreateForm()
		profile_form = ProfileCreateForm()

	return render(request, 'cms/create_user.html', {'user_form':user_form, 'profile_form':profile_form})

@login_required
@permission_required('auth.add_user', login_url='/login/')
def user_detail_view(request, id):
	template = 'cms/user_detail.html'
	user_obj = get_object_or_404(User, pk=id)
	profile_obj = get_object_or_404(Profile, pk=id)
	return render(request, template,  {'user_obj': user_obj, 'profile_obj': profile_obj})


def account_activation_sent(request):
	return render(request, 'cms/account_activation_sent.html')


def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except (TypeError, ValueError, OverFlowError, User.DoesNotExist):
		user = None

	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.profile.email_confirmed = True
		user.save()
		if user.is_staff:

			return redirect('cms_home')
		else:
			return render(request, 'cms/client_activation.html')
	else:
		return redirect(request, 'account_activation_invalid.html')

@login_required
@permission_required('reports.add_report', login_url='/login/')
def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)
			messages.success(request, 'Your password was successfully changed.')
			return redirect('cms_home')
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		form = PasswordChangeForm(request.user)

	return render(request, 'cms/change_password.html', {'form': form})


class DeleteUserView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
	permission_required = ('auth.add_user')
	model = User
	slug_field = 'pk'
	template_name = 'cms/delete_user.html'
	success_url = '/'
	success_message = "User was successfully deleted."

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

class ReportDetailView(PermissionRequiredMixin, DetailView):
	permission_required = ('reports.add_report')
	model = Report
	slug_field = 'pk'
	context_object_name = 'report'
	template_name = 'cms/report_detail.html'

class CreateReportView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
	permission_required = ('reports.add_report')
	model = Report
	template_name = 'cms/create_report.html'
	form_class = ReportForm
	
	success_url = '/'
	success_message = "Report was successfully created."

	def form_valid(self, form):
		title = form.cleaned_data['title']
		location = form.cleaned_data['location']
		is_flash = form.cleaned_data['send_flash']
		new_report = form.save()
		#print(('http://intel.issrisk.com/report/{id}/detail/').format(id=new_report.id))
		if is_flash:
			receivers = User.objects.filter(profile__sub_country__name__icontains=location)
			shortener = Shortener('Tinyurl', timeout=30)
			long_url = ('http://intel.issrisk.com/report/{id}/detail/').format(id=new_report.id)
			short_url = shortener.short(long_url)
			body = "ISSRISK | {location}:{title}. Access report at {url}".format(location=location, title=title, url=short_url)
			for item in receivers:
				if item.profile.phone_number == '':
					continue
				else:

					send_twilio_message(item.profile.phone_number, body)

		# send mail to subscribers on publish with html
		receivers = User.objects.filter(profile__sub_country__name__icontains=location).exclude(is_active=False)
		subject = "ISSRISK - New Report"
		rep_url = ('http://intel.issrisk.com/report/{id}/detail/').format(id=new_report.id)
		email_ctx = {
			'report': new_report,
			'url': rep_url,
		}
		message = get_template('cms/new_report.html').render(email_ctx)
		from_email = DEFAULT_FROM_EMAIL
		email_list = [item.email for item in receivers]

		def get_publish_email_list(email_list, subject, message):
			email_arr = []
			for email in email_list:
				mail_obj = mail.EmailMessage(
					subject,
					message,
					from_email,
					[email],
				)
				mail_obj.content_subtype = 'html'
				email_arr.append(mail_obj)

			return email_arr

		#send mail
		connection = mail.get_connection()
		email_messages = get_publish_email_list(email_list, subject, message)
		connection.send_messages(email_messages)


		return super(CreateReportView, self).form_valid(form)

class UpdateReportView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
	permission_required = ('reports.change_report')
	model = Report
	slug_field='pk'
	template_name = 'cms/update_report.html'
	form_class = ReportUpdateForm
	success_url = '/'
	success_message = "Report was successfully updated."

	def form_valid(self, form):

		rep = Report.objects.get(id=self.kwargs['pk'])
		rep_url = ('http://intel.issrisk.com/report/{id}/detail/').format(id=self.kwargs["pk"])
		is_major = form.cleaned_data['major_revision']
		loc = form.cleaned_data['location']
		
		queryset = User.objects.filter(profile__sub_country__name__icontains=loc)
		from_email = DEFAULT_FROM_EMAIL
		email_list = [item.email for item in queryset]
		subject = "Major revision for Report"
		ctx = {
			'rep': rep,
			'rep_url' : rep_url,
		}
		message = get_template('cms/report_update_email.html').render(ctx)
		def get_major_email(email_list, subject ,message):
			email_arr = []
			for email in email_list:
				mail_obj = mail.EmailMessage(
					subject,
					message,
					from_email,
					[email],
				)
				mail_obj.content_subtype = 'html'
				email_arr.append(mail_obj)

			return email_arr

		if is_major:
			connection = mail.get_connection()
			email_messages = get_major_email(email_list, subject, message)
			connection.send_messages(email_messages)

		return super(UpdateReportView, self).form_valid(form)

class DeleteReportView(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
	permission_required = ('reports.delete_report')
	model = Report
	slug_field = 'pk'
	template_name = 'cms/delete_report.html'
	success_url = '/'
	success_message = "Report was successfully deleted."

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

class CreateCountryView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
	permission_required = ('reports.add_country')
	model = Country
	template_name = 'cms/create_country.html'
	form_class = CountryForm
	success_url = '/'
	success_message = "Country was successfully created."

class UpdateCountryView(PermissionRequiredMixin,SuccessMessageMixin, UpdateView):
	permission_required = ('reports.change_country')
	model = Country
	slug_field = 'pk'
	template_name = 'cms/update_country.html'
	form_class = CountryForm
	success_url = '/'
	success_message = "Country was successfully updated."

class DeleteCountryView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
	permission_required = ('reports.delete_country')
	model = Country
	slug_field = 'pk'
	template_name = 'cms/delete_country.html'
	success_url = '/'
	success_message = "Country was successfully deleted."


	



		
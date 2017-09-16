from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import ListView, DetailView
from django.template.loader import render_to_string, get_template
from accounts.models import Profile

# from .filters import UserFilter
from .models import Report, Country
from .forms import ProfileUpdateForm, SearchForm,TrialSubProfileForm, TrialSubUserForm
from functools import reduce
import operator
from datetime import datetime, timedelta

# Create your views here.

def trial_sub_form(request):
	template = 'reports/trial_sub.html'
	if request.method == 'POST':
		user_form = TrialSubUserForm(request.POST)
		profile_form = TrialSubProfileForm(request.POST)
		if all([user_form.is_valid(), profile_form.is_valid()]):
			user = user_form.save()
			#activate trial user
			user.is_active = True
			user.profile.phone_number = profile_form.cleaned_data["phone_number"]
			user.profile.company = profile_form.cleaned_data["company"]
			user.profile.sub_country = profile_form.cleaned_data["sub_country"]
			user.profile.sub_model = profile_form.cleaned_data["sub_model"]
			user.profile.trial_sub = True

			# if trial_sub get current date and set end date 14/30 days from now()
			user.profile.valid_till = datetime.now().date() + timedelta(days=14)	

			#generate random password
			new_password = User.objects.make_random_password()
			user.set_password(new_password)
			user.save()
			user.profile.save()

			#get current site, subject for email
			current_site = get_current_site(request)
			subject = 'ISSRISK Trial Subscription'

			#email user with account cred
			message = render_to_string('reports/trial_activation_email.html', {
				'user': user,
				'domain': current_site.domain,
				'password': new_password
			})
			user.email_user(subject, message)
			
	else:
		user_form = TrialSubUserForm()
		profile_form = TrialSubProfileForm()

	return render(request, template, {'user_form': user_form, 'profile_form': profile_form})

@login_required
def user_profile_view(request):
	template = 'reports/user_profile.html'
	user = request.user
	profile = request.user.profile
	sub_type = profile.sub_model
	if (sub_type == "T"):
		sub = "Travel"
	elif (sub_type == "C"):
		sub = "Country"
	else:
		sub = "Travel and Country"

	return render(request, template, {'user': user, 'sub': sub})


@login_required
def user_profile_edit(request):
	if request.method == 'POST':
		form = ProfileUpdateForm(request.POST)
		if form.is_valid():
			# user = form.save()
			user = request.user
			user.profile.phone_number = form.cleaned_data["phone_number"]
			user.profile.sub_country = form.cleaned_data["sub_country"]
			user.profile.sub_model = form.cleaned_data["sub_model"]
			user.profile.company = form.cleaned_data["company"]
			user.profile.save()
			messages.success(request, 'Your password was successfully changed.')
			return redirect('home')
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		form = ProfileUpdateForm()

	return render(request, 'reports/change_password.html', {'form': form})



@login_required
def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)
			messages.success(request, 'Your password was successfully changed.')
			return redirect('home')
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		form = PasswordChangeForm(request.user)

	return render(request, 'reports/change_password.html', {'form': form})


@login_required
def index(request):
	user = request.user
	qs = Profile.objects.get(user=user)
	loc = qs.sub_country.all()
	rep_qs = [(Report.objects.filter(location__name__icontains=loc_obj.name).order_by('-updated_at')) for loc_obj in loc]
	reports = [item for sublist in rep_qs for item in sublist]


	return render(request, 'reports/index.html', {'loc':loc, 'rep_qs': reports})

class ReportListView(LoginRequiredMixin, ListView):
	model = Report
	#queryset = Report.objects.filter('-created_at')
	context_object_name = 'report_list'
	template_name = 'reports/report_list.html'

	# def get_queryset(self):
	# 	user = self.request.user
	# 	qs = Profile.objects.get(user=user)
	# 	loc = qs.sub_country.all()
	# 	sub_model = qs.sub_model
	# 	if (sub_model == 'T' or sub_model == 'C'):
	# 		rep_mod = Report.objects.filter(Q(report_type__exact=sub_model))
	# 	if (sub_model == 'TC'):
	# 		rep_mod = Report.objects.all()
	# def get_context_data(self, *args, **kwargs):
	# 	context = super(ReportListView, self).get_context_data(*args, **kwargs)
	# 	filtered

	# 	rep_qs = [(rep_mod.filter(Q(location__name__icontains=loc_obj.name)).order_by('updated_at')) for loc_obj in loc]
	# 	reports = [item for sublist in rep_qs for item in sublist]

	# 	return reports

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

	def get_context_data(self, **kwargs):
		context = super(CountryDetailView, self).get_context_data(**kwargs)
		rel_reps = Report.objects.filter(location__name__icontains=self.object.name).order_by('-created_at')
		context["rel_reps"] = rel_reps
		return context


def search(request):

	query = request.GET.get("q")
	loc = request.GET.get("l")
	rep_type = request.GET.get("t")
	from_date = request.GET.get("fd")
	to_date = request.GET.get("td")
	
	print(from_date, to_date)
	if not from_date == "":
		from_date_data = datetime.datetime.strptime(from_date, "%Y-%m-%d")
	else:
		from_date_data = None

	if not from_date == "":
		to_date_data = datetime.datetime.strptime(to_date, "%Y-%m-%d")
	else:
		to_date_data = None
	
	
	print(from_date_data, to_date_data)
	report_list = Report.objects.all()
	if loc is not None:
		report_list = report_list.filter(location__name__icontains=loc)
	if rep_type is not None:
		if rep_type == "T":
			report_list = report_list.filter(report_type__exact="T")
		elif rep_type == "C":
			report_list = report_list.filter(report_type__exact="C")
		else:
			report_list = report_list

	if from_date_data is not None:
		report_list = report_list.filter(created_at__gte=from_date_data)

	if to_date_data is not None:
		report_list = report_list.filter(created_at__lte=to_date_data)

	if query:

		query_list = query.split()
		result = report_list.filter(
			reduce(operator.and_, (Q(title__icontains=q) for q in query_list)) |
			reduce(operator.and_, (Q(summary__icontains=q) for q in query_list))
		).exclude(archive=True).order_by('-created_at')

	else:
		empty_msg = "Please Input a text to search. Empty Searches are not allowed."
		return render(request, 'reports/search.html', {'empty_msg': empty_msg})

	return render(request, 'reports/search.html', {'search_results': result})




# def account_activation_sent(request):
# 	return render(request, 'reports/account_activation_sent.html')


# def activate(request, uidb64, token):
# 	try:
# 		uid = force_text(urlsafe_base64_decode(uidb64))
# 		user = User.objects.get(pk=uid)
# 	except (TypeError, ValueError, OverFlowError, User.DoesNotExist):
# 		user = None

# 	if user is not None and account_activation_token.check_token(user, token):
# 		user.is_active = True
# 		user.profile.email_confirmed = True
# 		user.save()
# 		return redirect('home')
# 	else:
# 		return redirect(request, 'reports/account_activation_invalid.html')
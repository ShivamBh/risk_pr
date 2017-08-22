from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from accounts.models import Profile
from .models import Report, Country

from functools import reduce
import operator

# Create your views here.
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
		rel_reps = Report.objects.filter(location__name__icontains=self.object.name)
		context["rel_reps"] = rel_reps
		return context

def search(request):
	query = request.GET.get("q")
	report_list = Report.objects.all()
	if query:
		query_list = query.split()
		result = Report.objects.filter(
			reduce(operator.and_, (Q(title__icontains=q) for q in query_list)) |
			reduce(operator.and_, (Q(summary__icontains=q) for q in query_list))
		)

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
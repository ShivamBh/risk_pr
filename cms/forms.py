from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from reports.models import Report, Country
from accounts.models import Profile

class CMSLoginForm(forms.Form):
	username = forms.CharField(error_messages={'required': 'Please enter your username'})
	password = forms.CharField(widget=forms.PasswordInput)

class UserCreateForm(UserCreationForm):
	class Meta:
		model = User
		fields = (
			"first_name",
			"last_name",
			"email",
			"username",
			"password1",
			"password2",
			"is_active",
			"is_staff",
			)

class ProfileCreateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = (
			"phone_number",
			"company",
			"sub_country",
			"sub_model",
			"is_moderator",
			"is_publisher",
			)

class ReportForm(forms.ModelForm):

	class Meta:
		model = Report
		fields = (
			"location",
			"title",
			"summary",
			"assessment",
			"impact_tc",
			"advice",
			"event_bg_title",
			"event_bg_text",
			"latitude",
			"longitude",
			"impact_radius",
			"report_type",
					)

class ReportUpdateForm(forms.ModelForm):

	major_revision = forms.BooleanField()

	class Meta:
		model = Report
		fields = (
			"location",
			"title",
			"summary",
			"assessment",
			"impact_tc",
			"advice",
			"event_bg_title",
			"event_bg_text",
			"latitude",
			"longitude",
			"impact_radius",
			"report_type",
					)

class CountryForm(forms.ModelForm):
	class Meta:
		model = Country
		fields = (
			"name",
			"flag",
			"political_rating",
			"security_rating",
			"terror_rating",
			"travel_rating",
			"sec_level",
			"risk_bg",
			)

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = (
			"first_name",
			"last_name",
			"username",
			"email",
			"is_active"
			)

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = (
			"phone_number",
			"company",
			"sub_country",
			"sub_model",
			)
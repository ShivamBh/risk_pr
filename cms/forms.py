from django import forms
from django.contrib.auth.models import User

from reports.models import Report, Country
from accounts.models import Profile

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

class CountryForm(forms.ModelForm):
	class Meta:
		model = Country
		fields = (
			"name",
			"rating",
			"risk_bg",
			)

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = (
			"first_name",
			"last_name",
			"username",
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
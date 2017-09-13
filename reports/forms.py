from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from accounts.models import Profile

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = (
			"phone_number",
			"company",
			"sub_country",
			"sub_model",
			
			)

class SearchForm(forms.Form):
	from_date = forms.DateField()
	to_date = forms.DateField()

class TrialSubProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = (
			"phone_number",
			"company",
			"sub_country",
			"sub_model",
			)

class TrialSubUserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = (
			"username",
			"first_name",
			"last_name",
			"email",
			)
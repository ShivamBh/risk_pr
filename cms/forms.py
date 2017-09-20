from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from reports.models import Report, Country
from accounts.models import Profile

class DateInput(forms.DateInput):
	input_type = 'date'

class CMSLoginForm(forms.Form):
	username = forms.CharField(error_messages={'required': 'Please enter your username'})
	password = forms.CharField(widget=forms.PasswordInput)

class UserCreateForm(forms.ModelForm):
	email = forms.EmailField(max_length=254, help_text='Required. Insert a valid email address.')

	class Meta:
		model = User
		fields = (
			"first_name",
			"last_name",
			"email",
			"username",
			"is_staff",
			)
	def clean_email(self):

		email = self.cleaned_data.get('email')
		username = self.cleaned_data.get('username')
		if email and User.objects.filter(email=email).exclude(username=username).exists():
			raise forms.ValidationError('Email address already exists')
		return email

	# def __init__( self, ProfileCreateForm,  *args, **kwargs):
	# 	super(UserCreateForm, self).__init__(*args, **kwargs)
	# 	self.ProfileCreateForm = ProfileCreateForm

	# def clean(self):
	# 	if not self.cleaned_data['is_staff']:
	# 		self.ProfileCreateForm.fields['is_moderator'].widget.attrs['disabled'] = True
	# 		self.ProfileCreateForm.fields['is_publisher'].widget.attrs['disabled'] = True

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
			"valid_till"
			)
		widgets = {
			'valid_till': DateInput(attrs= {'type': 'date'}),
		}

class ReportForm(forms.ModelForm):
	send_flash = forms.BooleanField(required=False)

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

	major_revision = forms.BooleanField(required=False)

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
			"archive",
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
			"is_active",
			"is_staff",
			)

	def clean_email(self):
		email = self.cleaned_data.get('email')
		username = self.cleaned_data.get('username')
		if email and User.objects.filter(email=email).exclude(username=username).exists():
			raise forms.ValidationError('Email address already exists')
		return email



class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = (
			"phone_number",
			"company",
			"sub_country",
			"sub_model",
			"email_confirmed",
			"is_moderator",
			"is_publisher",
			"valid_till"
			)
		widgets = {
			'valid_till': DateInput(attrs= {'type': 'date'}),
		}
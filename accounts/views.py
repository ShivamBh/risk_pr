from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from riskproject.settings import DEFAULT_FROM_EMAIL
from django.views.generic import *
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.contrib.sites.shortcuts import get_current_site

from .models import Profile
from .forms import LoginForm


# Create your views here.
# def user_login(request):
# 	if request.method == 'POST':
# 		form = LoginForm(request.POST)
# 		if form.is_valid():
# 			cd = form.cleaned_data
# 			user = authenticate(username=cd['username'], password=cd['password'])

# 			if user is not None:
# 				if user.is_active:
# 					login(request, user)
# 					return HttpResponse('Auth Success')

# 				else:
# 					return HttpResponse('Disabled Account')

# 			else:
# 				return HttpResponse('Invalid Login')

# 	else:
# 		form = LoginForm()
# 	return render(request, 'accounts/home.html', {'form':form})


@login_required
def index(request):
	return render(request, 'accounts/home.html', {'section': 'dashboard'})

# class ResetPasswordRequestView(FormView):
# 	template_name = 'accounts/password_reset.html'
# 	success_url = '/login/'
# 	form_class = PasswordResetForm

# 	@staticmethod
# 	def validate_email_address(email):

# 		try:
# 			validate_email(email)
# 			return True
# 		except ValidationError:
# 			return False

# 	def post(self, request, *args, **kwargs):

# 		form = self.form_class(request.POST)
# 		if form.is_valid():
# 			data = form.cleaned_data["email"]
# 		if self.validate_email_address(data) is True:

# 			associated_user = User.objects.filter(Q(email=data))
# 			if associated_user.exists():
# 				for user in associated_user:
# 					c = {
# 						'email': user.email,
# 						'domain':get_current_site(request).domain,
# 						'site_name': 'mysite',
# 						'uid': urlsafe_base64_encode(force_bytes(user.pk)),
# 						'user': user,
# 						'token': default_token_generator.make_token(user),
# 						'protocol': 'http',
# 						}

# 					subject_template_name = 'registration/password_reset_subject.txt'
# 					email_template_name = 'registration/password_reset_email.html'
# 					subject = loader.render_to_string(subject_template_name, c)
# 					subject = ''.join(subject.splitlines())
# 					email = loader.render_to_string(email_template_name, c)
# 					send_mail(subject, email, DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)

# 				result = self.form_valid(form)
# 				messages.success(request, 'An email has been sent to ' + data + '. Please check your inbox(and spam folders) to continue resetting the password')
# 				return result

# 			result = self.form_invalid(form)
# 			messages.error(request, 'No user is associated with this email address. Contact admin for help.')
# 			return result



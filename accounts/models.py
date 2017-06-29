from django.db import models
from django.db.models import CharField
from django.contrib.auth.models import User

from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.db.models.signals import class_prepared
from django.dispatch import receiver

from reports.models import Country

# Create your models here.

class Profile(models.Model):
	
	SUB_MODEL_CHOICES = (
		('T', 'Travel'),
		('C', 'Country'),
		('TC', 'Travel & Country'),
	)

	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=20)
	#contact_no = models.CharField(max_length=20, blank=False, default="12345")
	company = models.CharField(max_length=120, blank=False, default="Company")
	sub_country = models.ManyToManyField(Country)
	sub_model = models.CharField(
		max_length=3,
		choices=SUB_MODEL_CHOICES,
		default="T",
	)

	def __str__(self):
		return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()

# @receiver(post_save, sender=Country)
# def add_country_field(sender, instance, created, **kwargs):
# 	if created:
# 		Profile.add_to_class("country", models.CharField(max_length=100))

# def add_field(sender, **kwargs):
# 	if sender.__name__ == "Country":
# 		field = CharField("New Field", max_length=100)
# 		field.contribute_to_class(sender, "name")

# class_prepared.connect(add_field)
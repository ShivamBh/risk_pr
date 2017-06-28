from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from reports.models import Country

# Create your models here.

class Profile(models.Model):
	clist = Country.objects.values_list('name', flat=True)
	SUB_MODEL_CHOICES = (
		('T', 'Travel'),
		('C', 'Country'),
		('TC', 'Travel & Country'),
	)

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	contact_no = models.CharField(max_length=20, blank=False, default="12345")
	company = models.CharField(max_length=120, blank=False, default="Company")
	#sub_country = models.ModelChoiceField(queryset=clist)
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
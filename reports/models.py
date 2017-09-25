from django.db import models
from tinymce.models import HTMLField
# Create your models here.
class Country(models.Model):
	RATING_CHOICES = (
		('L', 'Low'),
		('M', 'Medium'),
		('H', 'High'),
		('Ex', 'Extreme'),
	)
	SEC_RATING_CHOICES = (
		('Green', 'Green'),
		('Yellow', 'Yellow'),
		('Amber', 'Amber'),
		('Red', 'Red'),
	)

	name = models.CharField(max_length=100, blank=False, null=False)
	flag = models.FileField(upload_to='flags', null=True)
	political_rating = models.CharField(
		max_length=2,
		choices = RATING_CHOICES,
		null=True,
	)
	security_rating = models.CharField(
		max_length=2,
		choices = RATING_CHOICES,
		null=True,
	)
	terror_rating = models.CharField(
		max_length=2,
		choices = RATING_CHOICES,
		null=True,
	)
	travel_rating = models.CharField(
		max_length=2,
		choices = RATING_CHOICES,
		null=True,
	)
	sec_level = models.CharField(
		max_length=10,
		choices = SEC_RATING_CHOICES,
		null=True,
	)

	risk_bg = HTMLField()

	def __str__(self):
		return self.name


class Report(models.Model):
	SUB_MODEL_CHOICES = (
		('T', 'Travel'),
		('C', 'Country'),
	)
	location = models.ForeignKey(Country, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	title = models.CharField(max_length=500, blank=False, null=False)
	# summary = models.TextField(blank=False, null=False)
	summary = HTMLField(blank=True)
	assessment = HTMLField(blank=True)
	impact_tc = models.CharField(max_length=500, blank=True)
	advice = HTMLField(blank=True)
	event_bg_title = models.CharField(max_length=300,blank=True)
	event_bg_text = HTMLField(blank=True)
	
	latitude = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True) 
	longitude = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
	impact_radius = models.IntegerField(blank=True, null=True)
	report_type = models.CharField(
		max_length=3,
		choices=SUB_MODEL_CHOICES, 
		default="T",
	)
	archive = models.BooleanField(default=False)

	def __str__(self):
		return self.title



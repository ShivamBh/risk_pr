from django.db import models

# Create your models here.
class Country(models.Model):
	RATING_CHOICES = (
		('L', 'Low'),
		('M', 'Medium'),
		('H', 'High'),
		('Ex', 'Extreme'),
	)
	name = models.CharField(max_length=100, blank=False, null=False)
	#flag = models.ImageField(upload_to='flags')
	rating = models.CharField(
		max_length=2,
		choices = RATING_CHOICES,
	)
	risk_bg = models.TextField()

	def __str__(self):
		return self.name


class Report(models.Model):
	location = models.ForeignKey(Country, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	title = models.CharField(max_length=500, blank=False, null=False)
	summary = models.TextField()
	assessment = models.TextField()
	impact_tc = models.CharField(max_length=500, blank=False, null=False)
	advice = models.TextField()
	event_bg_title = models.CharField(max_length=300, blank=False, null=False)
	event_bg_text = models.TextField()
	
	latitude = models.DecimalField(max_digits=10, decimal_places=4)
	longitude = models.DecimalField(max_digits=10, decimal_places=4)
	impact_radius = models.IntegerField()
	report_type = models.CharField(max_length=25, blank=False, null=False)

	def __str__(self):
		return self.title



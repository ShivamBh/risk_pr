from django.db import models

# Create your models here.
class FlashMessage(models.Model):
	to_number = models.CharField(max_length=30)
	from_number = models.CharField(max_length=30)
	location = models.CharField(max_length=100, blank=False)
	body = models.CharField(max_length=160)
	sms_sid = models.CharField(max_length=34, default="", blank=True)
	account_sid = models.CharField(max_length=34, default="", blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	sent_at = models.DateTimeField(null=True, blank=True)
	delivered_at = models.DateTimeField(null=True, blank=True)
	status = models.CharField(max_length=20, default="", blank=True)



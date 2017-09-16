from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from datetime import datetime, timedelta
from django.template.loader import render_to_string
from django.contrib.auth.models import User

logger = get_task_logger(__name__)

@periodic_task(
	run_every=(crontab(minute=0, hour=0)),
	name="check_trial_sub",
	ignore_result=True
)
def task_check_trial_sub():

	def send_notfication_mail(days, user_obj):
		subject = 'Account Activation - ISSRISK'

		message = render_to_string('accounts/subscription_notice.html' , {
			'user': user_obj,
			'days': days
		})
		user = user_obj
		user.email_user(subject, message)

	#iterate through profiles, check validity and send mail
	today = datetime.now().date()
	queryset = User.objects.filter(is_staff=False)
	for obj in queryset:
		# check if user is a trial user
		print('yolo')
		if obj.profile.valid_till is not None:

			user_email = obj.email
			user = obj
			print('yolo2')
			# 7 day notification
			if (obj.profile.valid_till.date() - today) == timedelta(7):
				# send 7 days left notice
				days = 7
				send_notfication_mail(days, obj)
				print('yolomail')

			if (obj.profile.valid_till.date() - today) == timedelta(2):
				# send 2 days left notice
				days = 2
				send_notfication_mail(days, obj)
				print('yolomail2')

			if (obj.profile.valid_till.date() - today) == timedelta(-1):
				# switch active flag, send email, acc deactivated
				days = -1
				obj.is_active = False
				send_notfication_mail(days, obj)

			


	print('running this biyaatch!')
	logger.info("Check once")


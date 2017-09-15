from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

# from .models import Profile

logger = get_task_logger(__name__)

@periodic_task(
	run_every=(crontab(minute='*')),
	name="check_trial_sub",
	ignore_result=True
)
def task_check_trial_sub():

	#do stuff
	logger.info("Check once")


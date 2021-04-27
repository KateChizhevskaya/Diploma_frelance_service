from celery.task import task
from django.core.mail import send_mail

from diploma.apps.tasks.constants import SITE_EMAIL


@task
def send_email(header, text, user=None, user_email=None):
	if not user_email and user:
		user_email = user.email
	send_mail(header, text, SITE_EMAIL, (user_email, ), fail_silently=False)


@task
def send_mails_to_many_users(header, text, users=None, users_mails=None):
	if not users_mails and users:
		users_mails = (user.email for user in users)
	send_mail(header, text, SITE_EMAIL, users_mails, fail_silently=False)

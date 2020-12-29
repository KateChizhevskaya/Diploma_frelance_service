from django.core.mail import send_mail
from celery import shared_task

from diploma.apps.tasks.constants import SITE_EMAIL


@shared_task
def send_email(header, text, user):
	send_mail(header, text, SITE_EMAIL, (user.email, ), fail_silently=False)


@shared_task
def send_mails_to_many_users(header, text, users=None, users_mails=None):
	if not users_mails and users:
		users_mails = (user.email for user in users)
	send_mail(header, text, SITE_EMAIL, users_mails, fail_silently=False)

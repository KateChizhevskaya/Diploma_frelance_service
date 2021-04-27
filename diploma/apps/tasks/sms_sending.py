from sms import send_sms

from diploma.apps.tasks.constants import OWNER_PHONE_NUMBER
from django.conf import settings
from twilio.rest import Client


def send_sms_task(code, phone_number):
	send_sms(
		f'Hello, your verification code is {code}',
		OWNER_PHONE_NUMBER,
		[phone_number, ],
		fail_silently=False
	)
	'''
	account_sid = settings.TWILIO_ACCOUNT_SID
	auth_token = settings.TWILIO_AUTH_TOKEN
	client = Client(account_sid, auth_token)

	client.messages.create(
		body=f'Hello, your verification code is {code}',
		from_=OWNER_PHONE_NUMBER,
		to=phone_number
	)
	'''
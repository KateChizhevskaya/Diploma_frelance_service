from django.db import models
from django.db.models import Q
from phonenumber_field.modelfields import PhoneNumberField


class VerificationClass(models.Model):
	email = models.EmailField(
		null=True
	)
	phone = PhoneNumberField(
		help_text='Contact phone number',
		null=True,
		region='BY'
	)
	sending_time = models.DateTimeField(
		auto_now_add=True
	)
	is_authorize = models.BooleanField(
		default=False
	)
	authorizing_time = models.DateTimeField()
	code_hash = models.CharField(
		max_length=128,
		blank=True,
		null=True
	)

	class Meta:
		constraints = [
			models.CheckConstraint(
				check=Q(email__isnull=False) | Q(phone__isnull=False),
				name='not_both_phone_email_null_verification_class'
			)
		]

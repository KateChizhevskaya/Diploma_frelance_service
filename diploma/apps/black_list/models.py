from django.db import models
from django.db.models import CASCADE, Q
from phonenumber_field.modelfields import PhoneNumberField


class BlackList(models.Model):
	address = models.CharField(
		max_length=100,
		blank=True,
		null=True,
		default=None
	)
	email = models.EmailField(
		null=True
	)
	phone = PhoneNumberField(
		help_text='Contact phone number',
		null=True,
		region='BY'
	)

	class Meta:
		constraints = [
			models.CheckConstraint(
				check=Q(email__isnull=False) | Q(phone__isnull=False),
				name='not_both_phone_email_null_bl_list'
			)
		]
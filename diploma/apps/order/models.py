from django.contrib.postgres.fields import ArrayField
from django.db.models import CASCADE, SET_NULL, Q
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from diploma.apps.order.constants import Statuses
from diploma.apps.works.models import Work


class WorkOrder(models.Model):
	work = models.ForeignKey(
		Work,
		related_name='work_requests',
		on_delete=SET_NULL,
		null=True
	)
	customer_email = models.EmailField(
		null=True
	)
	customer_phone = PhoneNumberField(
		help_text='Contact phone number',
		null=True,
		region='BY'
	)
	date_of_creating_request = models.DateTimeField(
		auto_now_add=True
	)
	status = models.CharField(
		max_length=20,
		choices=Statuses.choices,
		default=Statuses.IN_PROCESS
	)
	customer_text_comment = models.CharField(
		max_length=100,
		blank=True,
		null=True,
		default=None
	)
	photos = ArrayField(
		models.ImageField(upload_to='request_photos/'),
		size=5,
		blank=True,
		null=True
	)
	date_time_of_work_begin = models.DateTimeField()
	address = models.CharField(
		max_length=100,
		blank=True,
		null=True,
		default=None
	)

	class Meta:
		constraints = [
			models.CheckConstraint(
				check=Q(customer_email__isnull=False) | Q(customer_phone__isnull=False),
				name='not_both_phone_email_null'
			)
		]
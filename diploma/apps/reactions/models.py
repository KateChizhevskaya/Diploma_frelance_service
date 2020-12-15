from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import CASCADE, SET_NULL
from django.db import models

from diploma.apps.reactions.constants import Statuses
from diploma.apps.user.models import MasterUser
from diploma.apps.works.models import Work


class Review(models.Model):
	work = models.ForeignKey(
		Work,
		related_name='reviews',
		on_delete=CASCADE
	)
	text = models.TextField(
		max_length=500,
		null=True,
		blank=True
	)
	rating = models.IntegerField(
		validators=[MinValueValidator(0), MaxValueValidator(5)],
		null=True
	)
	user = models.ForeignKey(
		MasterUser,
		related_name='reviews',
		on_delete=CASCADE
	)
	date = models.DateField(
		auto_now=True
	)
	photos = ArrayField(
		models.ImageField(upload_to='review_photos/'),
		size=5,
		blank=True,
		null=True
	)


class Complaint(models.Model):
	complaint_creater = models.ForeignKey(
		MasterUser,
		related_name='complaints_created',
		on_delete=CASCADE
	)
	defendant_email = models.EmailField()
	text = models.TextField(
		max_length=500
	)
	photos = ArrayField(
		models.ImageField(upload_to='complaint_photos/'),
		size=5,
		blank=True,
		null=True
	)
	documents = ArrayField(
		models.FileField(upload_to='complaint_documents/'),
		size=5,
		blank=True,
		null=True
	)
	status = models.CharField(
		max_length=20,
		choices=Statuses.choices,
		default=Statuses.IN_PROCESS
	)

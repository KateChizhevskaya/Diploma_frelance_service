from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import CASCADE
from django.utils.timezone import now

from diploma.apps.user.models import MasterUser
from diploma.apps.works.models import Work


class Portfolio(models.Model):
	additional_description = models.TextField(
		max_length=500,
		blank=True,
		null=True
	)
	work = models.ForeignKey(
		Work,
		related_name='portfolios',
		on_delete=CASCADE
	)
	master = models.ForeignKey(
		MasterUser,
		related_name='portfolios',
		on_delete=CASCADE
	)
	photos = ArrayField(
		models.ImageField(upload_to='portfolio_photos/'),
		size=5,
		blank=True,
		null=True
	)
	price = models.FloatField(
		validators=[MinValueValidator(0.01), MaxValueValidator(10000)]
	)
	spending_hours = models.FloatField(
		validators=[MinValueValidator(0.01), MaxValueValidator(1000)]
	)

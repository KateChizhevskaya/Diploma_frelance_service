from django.db import models
from django.utils.timezone import now


class Portfolio(models.Model):
	additional_description = models.TextField(
		max_length=500,
		blank=True,
		null=True
	)

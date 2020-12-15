from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from diploma.apps.works.constants import PlaceNames, WorkName


class Work(models.Model):
	comment = models.TextField(
		max_length=150,
	)
	placement = models.CharField(
		max_length=20,
		choices=PlaceNames.choices,
		default=PlaceNames.IN_PLACE
	)
	name = models.CharField(
		max_length=50,
		choices=WorkName.choices
	)
	nim_cost_with_materials = models.FloatField(
		validators=[MinValueValidator(0.01), MaxValueValidator(10000)]
	)
	nim_cost_without_materials = models.FloatField(
		validators=[MinValueValidator(0.01), MaxValueValidator(10000)]
	)

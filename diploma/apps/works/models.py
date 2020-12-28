from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import CASCADE

from diploma.apps.user.models import MasterUser
from diploma.apps.works.constants import PlaceNames, WorkName, MaterialsNeed


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
		validators=[MinValueValidator(0.01), MaxValueValidator(10000)],
		null=True
	)
	nim_cost_without_materials = models.FloatField(
		validators=[MinValueValidator(0.01), MaxValueValidator(10000)],
		null=True
	)
	worker = models.ForeignKey(
		MasterUser,
		related_name='works',
		on_delete=CASCADE
	)
	need_materials = models.CharField(
		max_length=5,
		choices=MaterialsNeed.choices,
		default=MaterialsNeed.NO
	)


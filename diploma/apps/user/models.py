from django.contrib.auth.models import AbstractUser
from django.db.models import BooleanField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class MasterUser(AbstractUser):
	is_deleted = BooleanField(default=False)
	phone_number = PhoneNumberField(
		help_text='Contact phone number',
		null=True,
		region='BY'
	)
	photo = models.ImageField(
		blank=True,
		null=True,
		default=None,
		upload_to='photos/'
	)
	rating = models.FloatField(
		validators=[MinValueValidator(0), MaxValueValidator(5)],
		default=0
	)



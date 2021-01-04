from django.db import models
from django.utils.translation import gettext_lazy as _


class Statuses(models.TextChoices):
	IN_PROCESS = 'in process', _('In process')
	APPROVED = 'approved', _('Approved')
	REJECTED = 'rejected', _('Rejected')


NOT_ACTIVE_STATUS = {Statuses.APPROVED, Statuses.REJECTED}

REVIEW_PHOTO_DIR = 'review_photos'
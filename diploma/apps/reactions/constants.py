from django.db import models
from django.utils.translation import gettext_lazy as _


class Statuses(models.TextChoices):
	IN_PROCESS = 'in process', _('In process')
	APPROVED = 'approved', _('Approved')
	REJECTED = 'rejected', _('Rejected')


NOT_ACTIVE_STATUS = {Statuses.APPROVED, Statuses.REJECTED}

REVIEW_PHOTO_DIR = 'review_photos'

COMPLAINT_PHOTO_DIR = 'complaint_photos'
COMPLAINT_DOCUMENT_DIR = 'complaint_documents'

COMPLAINT_HEADER = 'Domestic service complaint'
COMPLAINT_TEXT = 'Your complaint is in system, please wait your administrator reaction'
COMPLAINT_ADMIN_TEXT = 'NEW COMPLAINT IS IN SYSTEM'

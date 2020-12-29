import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _


class Statuses(models.TextChoices):
	IN_PROCESS = 'in process', _('In process')
	APPROVED = 'approved', _('Approved')
	REJECTED = 'rejected', _('Rejected')


ACTIVE_STATUS = {Statuses.APPROVED, Statuses.IN_PROCESS}
BUFFER_PERIOD = datetime.timedelta(minutes=30)

ORDER_REQUEST_HEADER = 'You have new order'
ORDER_REQUEST_TEXT = 'Please, react to new order'

ORDER_PHOTO_DIR = 'order_photos'

from django.db import models
from django.utils.translation import gettext_lazy as _


class WorkName(models.TextChoices):
	FIX_COMPUTER = 'fix computer', _('Fix computer')
	FIX_FAUCET = 'fix faucet', _('Fix faucet')
	CLEAN_HOUSE = 'clean house', _('Clean house')
	INSTALL_WINDOWS = 'install windows', _('Install windows')
	CLEAN_SOFA = 'clean sofa', _('Clean sofa')


class PlaceNames(models.TextChoices):
	IN_PLACE = 'in place', _('In place')
	NOT_IN_PLACE = 'not in place', _('Not in place')


class MaterialsNeed(models.TextChoices):
	YES = 'yes', _('Yes')
	NO = 'no', _('No')
	BOTH = 'both', _('Both')


WORK_CHANGE_HEADER = 'Domestic services work change'
WORK_TEXT_START = 'Please note that the work '
WORK_CHANGE_TEXT_END = 'has changed, contact your contractor for details'

WORK_DELETE_HEADER = 'Domestic services work delete'
WORK_DELETE_TEXT_END = 'has deleted, contact your contractor for details'

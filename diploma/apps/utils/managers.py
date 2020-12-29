from django.db import models

from diploma.apps.order.constants import Statuses


class ActiveWorkManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(worker__is_deleted=False, is_deleted=False)


class UnapprovedOrderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Statuses.IN_PROCESS)

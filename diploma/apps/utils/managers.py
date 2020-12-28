from django.db import models


class ActiveWorkManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(worker__is_deleted=False, is_deleted=False)
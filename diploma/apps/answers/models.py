from django.db import models
from django.db.models import CASCADE

from diploma.apps.order.models import WorkOrder
from diploma.apps.reactions.models import Complaint
from diploma.apps.user.models import MasterUser


class ComplaintAnswer(models.Model):
	comlaint = models.ForeignKey(
		Complaint,
		related_name='complaints_answer',
		on_delete=CASCADE
	)
	answered_admin = models.ForeignKey(
		MasterUser,
		related_name='complaints_answer',
		on_delete=CASCADE
	)
	text = models.TextField(
		max_length=500
	)


class OrderAnswer(models.Model):
	order = models.ForeignKey(
		WorkOrder,
		related_name='order_answer',
		on_delete=CASCADE
	)
	text = models.TextField(
		max_length=500
	)

import django_filters
from django.db.models import Q
from django_filters import rest_framework

from diploma.apps.order.constants import Statuses
from diploma.apps.order.models import WorkOrder
from diploma.apps.works.models import Work


class WorkFilter(django_filters.FilterSet):

	class Meta:
		model = Work
		fields = {
			'nim_cost_with_materials': ['lt', 'gt'],
			'nim_cost_without_materials': ['lt', 'gt'],
			'placement': ['in'],
			'name': ['in'],
		}

import factory
from django.utils import timezone

from diploma.apps.order.factories import OrderFactory
from diploma.tests.test_apps.test_answer.constants import TEST_TEXT


class OrderAnswerFactory(factory.django.DjangoModelFactory):
	order = OrderFactory()
	text = TEST_TEXT

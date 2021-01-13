import factory

from diploma.apps.answers.models import OrderAnswer
from diploma.apps.order.factories import OrderFactory
from diploma.tests.test_apps.test_answer.constants import TEST_TEXT


class OrderAnswerFactory(factory.django.DjangoModelFactory):
	order = OrderFactory()
	text = TEST_TEXT

	class Meta:
		model = OrderAnswer

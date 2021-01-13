import factory
from django.utils import timezone
from diploma.apps.works.factories import WorkFactory


class OrderFactory(factory.django.DjangoModelFactory):
	work = WorkFactory()
	customer_email = factory.Faker('email')
	date_time_of_work_begin = timezone.now()

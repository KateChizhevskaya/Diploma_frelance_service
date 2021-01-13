import factory

from diploma.apps.reactions.models import Review, Complaint


class ReviewFactory(factory.django.DjangoModelFactory):
	text = factory.Faker('pystr', max_chars=10)

	class Meta:
		model = Review


class ComplaintFactory(factory.django.DjangoModelFactory):
	text = factory.Faker('pystr', max_chars=10)
	defendant_email = factory.Faker('email')

	class Meta:
		model = Complaint

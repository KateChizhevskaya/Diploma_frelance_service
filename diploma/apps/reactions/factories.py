import factory

from diploma.apps.reactions.models import Review


class ReviewFactory(factory.django.DjangoModelFactory):
	text = factory.Faker('pystr', max_chars=10)

	class Meta:
		model = Review


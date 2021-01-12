import factory

from diploma.apps.user.models import MasterUser


class UserFactory(factory.django.DjangoModelFactory):
	email = factory.Faker('email')
	username = factory.Faker('email')
	password = factory.PostGenerationMethodCall('set_password', 'kate_user')
	first_name = factory.Faker('first_name')
	last_name = factory.Faker('last_name')
	is_staff = False
	is_active = True
	is_master = False
	is_superuser = False

	class Meta:
		model = MasterUser

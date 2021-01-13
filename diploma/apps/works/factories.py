import factory

from diploma.apps.works.constants import PlaceNames, WorkName, MaterialsNeed
from diploma.apps.works.models import Work


class WorkFactory(factory.django.DjangoModelFactory):
	comment = factory.Faker('pystr', max_chars=10)
	placement = PlaceNames.IN_PLACE
	name = WorkName.FIX_COMPUTER
	nim_cost_with_materials = factory.Faker(
		'random_int', min=1, max=10
	)
	need_materials = MaterialsNeed.YES
	is_deleted = False
	rating = factory.Faker(
		'random_int', min=1, max=4
	)

	class Meta:
		model = Work

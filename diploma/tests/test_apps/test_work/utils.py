import random

from diploma.apps.works.constants import WorkName, PlaceNames, MaterialsNeed
from diploma.apps.works.models import Work


def get_base_work():
	return {
		'name': WorkName.FIX_COMPUTER,
		'placement': PlaceNames.IN_PLACE
	}


def get_work_with_incorrect_price():
	work = get_base_work()
	work['need_materials'] = MaterialsNeed.NO
	work['nim_cost_with_materials'] = random.uniform(1.0, 10)
	return work


def get_work_with_correct_price():
	work = get_base_work()
	work['need_materials'] = MaterialsNeed.YES
	work['nim_cost_with_materials'] = random.uniform(1.0, 10)
	return work


def create_work_with_need_materials(user):
	work = get_work_with_correct_price()
	work['worker'] = user
	return Work.objects.create(**work)


def incorrect_update_for_work_with_need_materials():
	return {
		'need_materials': "no"
	}


def correct_update_for_work_with_need_materials():
	return {
		'need_materials': "no",
		'nim_cost_without_materials': random.uniform(1.0, 10)
	}

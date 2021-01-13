from diploma.tests.test_apps.test_order.utils import get_correct_unapproved_order, get_correct_approved_order
from diploma.tests.test_apps.test_work.utils import create_work_with_need_materials


def get_base_review(work, rating):
	return {
		'work': work.id,
		'rating': rating
	}


def get_base_review_update(rating):
	return {
		'rating': rating
	}


def create_order_for_answer(user, master_user):
	work = create_work_with_need_materials(master_user)
	get_correct_approved_order(work, user)
	return work


def create_incorrect_order_for_answer(user, master_user):
	work = create_work_with_need_materials(master_user)
	get_correct_unapproved_order(work, user)
	return work


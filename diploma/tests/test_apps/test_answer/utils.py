from diploma.apps.reactions.constants import Statuses
from diploma.tests.test_apps.test_answer.constants import TEST_TEXT
from diploma.tests.test_apps.test_order.utils import get_correct_unapproved_order
from diploma.tests.test_apps.test_work.utils import create_work_with_need_materials


def get_base_order_answer(order, text, status):
	return {
		'order': order.id,
		'text': text,
		'status': status
	}


def get_base_complaint_answer(complaint, text, status):
	return {
		'complaint': complaint.id,
		'text': text,
		'status': status
	}


def get_correct_order_answer(order):
	return get_base_order_answer(order, TEST_TEXT, Statuses.APPROVED)


def get_incorrect_order_answer(order):
	return get_base_order_answer(order, TEST_TEXT, Statuses.IN_PROCESS)


def get_correct_complaint_answer(complaint):
	return get_base_complaint_answer(complaint, TEST_TEXT, Statuses.APPROVED)


def get_incorrect_complaint_answer(complaint):
	return get_base_complaint_answer(complaint, TEST_TEXT, Statuses.IN_PROCESS)


def create_order_for_answer(user, master_user):
	work = create_work_with_need_materials(master_user)
	return get_correct_unapproved_order(work, user)

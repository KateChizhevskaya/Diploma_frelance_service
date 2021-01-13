from dateutil.relativedelta import relativedelta
from django.utils import timezone

from diploma.apps.black_list.models import BlackList
from diploma.apps.order.constants import Statuses
from diploma.apps.order.models import WorkOrder
from diploma.tests.test_apps.test_order.constants import INCORRECT_PERIOD_FOR_TESTS, CORRECT_PERIOD_FOR_TESTS, \
	TEST_COMMENT
from diploma.tests.test_apps.test_work.utils import create_work_with_need_materials


def get_base_order(work):
	return {
		'work': work.id,
		'date_time_of_work_begin': timezone.now() + relativedelta(minutes=1)
	}


def get_base_update_order():
	return {
		'customer_text_comment': TEST_COMMENT
	}


def create_order(work, time, email, status):
	return WorkOrder.objects.create(
		work=work,
		date_time_of_work_begin=time,
		customer_email=email,
		status=status
	)


def get_order_with_incorrect_time(work, user):
	create_order(work, timezone.now() - INCORRECT_PERIOD_FOR_TESTS, user.email, Statuses.APPROVED)
	return get_base_order(work)


def get_order_with_black_list(work, user):
	BlackList.objects.create(email=user.email)
	create_order(work, timezone.now() - CORRECT_PERIOD_FOR_TESTS, user.email, Statuses.APPROVED)
	return get_base_order(work)


def get_correct_order(work, user):
	create_order(work, timezone.now() - CORRECT_PERIOD_FOR_TESTS, user.email, Statuses.APPROVED)
	return get_base_order(work)


def get_correct_unapproved_order(work, user):
	return create_order(work, timezone.now() - CORRECT_PERIOD_FOR_TESTS, user.email, Statuses.IN_PROCESS)


def get_correct_approved_order(work, user):
	return create_order(work, timezone.now() - CORRECT_PERIOD_FOR_TESTS, user.email, Statuses.APPROVED)

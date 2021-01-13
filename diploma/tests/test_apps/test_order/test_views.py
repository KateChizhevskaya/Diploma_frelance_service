import pytest
from rest_framework import status as rest_status

from diploma.apps.order.models import WorkOrder
from diploma.tests.test_apps.test_order.constants import TEST_COMMENT
from diploma.tests.test_apps.test_order.utils import get_correct_order, get_order_with_incorrect_time, \
	get_order_with_black_list, get_correct_unapproved_order, get_base_update_order, get_correct_approved_order
from diploma.tests.test_apps.test_work.utils import create_work_with_need_materials
from diploma.tests.utils import post_data, patch_data, del_response


@pytest.mark.django_db
def test_create_order_ok(user, master_user):
	work = create_work_with_need_materials(master_user)
	order = get_correct_order(work, user)
	response = post_data(user, 'order_create', data=order)
	assert response.status_code == rest_status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_order_fail(user, master_user):
	work = create_work_with_need_materials(master_user)
	order = get_order_with_incorrect_time(work, user)
	response = post_data(user, 'order_create', data=order)
	assert response.status_code == rest_status.HTTP_400_BAD_REQUEST
	order = get_order_with_black_list(work, user)
	response = post_data(user, 'order_create', data=order)
	assert response.status_code == rest_status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_update_order_ok(user, master_user):
	work = create_work_with_need_materials(master_user)
	order = get_correct_unapproved_order(work, user)
	update_dict = get_base_update_order()
	response = patch_data(user, 'order_update', data=update_dict, id=order.id)
	assert response.status_code == rest_status.HTTP_200_OK
	assert WorkOrder.objects.first().customer_text_comment == TEST_COMMENT


@pytest.mark.django_db
def test_update_order_fail(user, master_user):
	work = create_work_with_need_materials(master_user)
	order = get_correct_unapproved_order(work, user)
	update_dict = get_base_update_order()
	response = patch_data(master_user, 'order_update', data=update_dict, id=order.id)
	assert response.status_code == rest_status.HTTP_400_BAD_REQUEST
	order = get_correct_approved_order(work, user)
	response = patch_data(user, 'order_update', data=update_dict, id=order.id)
	assert response.status_code == rest_status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_remove_order_ok(user, master_user):
	work = create_work_with_need_materials(master_user)
	order = get_correct_unapproved_order(work, user)
	response = del_response(user, 'order_remove', id=order.id)
	assert response.status_code == rest_status.HTTP_204_NO_CONTENT
	assert WorkOrder.objects.count() == 0


@pytest.mark.django_db
def test_remove_order_fail(user, master_user):
	work = create_work_with_need_materials(master_user)
	order = get_correct_unapproved_order(work, user)
	response = del_response(master_user, 'order_remove', id=order.id)
	assert response.status_code == rest_status.HTTP_400_BAD_REQUEST
	order = get_correct_approved_order(work, user)
	response = del_response(user, 'order_remove', id=order.id)
	assert response.status_code == rest_status.HTTP_400_BAD_REQUEST

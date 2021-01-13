import pytest
from rest_framework import status as rest_status

from diploma.tests.test_apps.test_answer.utils import get_correct_order_answer, create_order_for_answer, \
	get_incorrect_order_answer
from diploma.tests.utils import post_data


@pytest.mark.django_db
def test_create_order_answer_ok(user, master_user):
	order = create_order_for_answer(user, master_user)
	order_answer_dict = get_correct_order_answer(order)
	response = post_data(master_user, 'order_answer_create', data=order_answer_dict)
	assert response.status_code == rest_status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_order_answer_failed(user, master_user):
	order = create_order_for_answer(user, master_user)
	order_answer_dict = get_incorrect_order_answer(order)
	response = post_data(master_user, 'order_answer_create', data=order_answer_dict)
	assert response.status_code == rest_status.HTTP_400_BAD_REQUEST
	order_answer_dict = get_correct_order_answer(order)
	response = post_data(user, 'order_answer_create', data=order_answer_dict)
	assert response.status_code == rest_status.HTTP_403_FORBIDDEN

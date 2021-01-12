import pytest
from rest_framework import status as rest_status

from diploma.apps.works.models import Work
from diploma.tests.test_apps.test_work.utils import get_work_with_correct_price, get_work_with_incorrect_price, \
	create_work_with_need_materials, correct_update_for_work_with_need_materials, \
	incorrect_update_for_work_with_need_materials
from diploma.tests.utils import post_data, patch_data, del_response


@pytest.mark.django_db
def test_create_work_ok(master_user):
	work = get_work_with_correct_price()
	response = post_data(master_user, 'work_create', data=work)
	assert response.status_code == rest_status.HTTP_201_CREATED
	assert Work.objects.count() == 1


@pytest.mark.django_db
def test_create_work_fail(master_user, user):
	work = get_work_with_incorrect_price()
	response = post_data(master_user, 'work_create', data=work)
	assert response .status_code == rest_status.HTTP_400_BAD_REQUEST
	assert Work.objects.count() == 0
	response = post_data(user, 'work_create', data=work)
	assert response .status_code == rest_status.HTTP_403_FORBIDDEN
	assert Work.objects.count() == 0


@pytest.mark.django_db
def test_update_work_ok(master_user):
	work = create_work_with_need_materials(master_user)
	update_dict = correct_update_for_work_with_need_materials()
	response = patch_data(master_user, 'work_update', data=update_dict, id=work.id)
	assert response.status_code == rest_status.HTTP_200_OK


@pytest.mark.django_db
def test_update_work_fail(master_user, user):
	work = create_work_with_need_materials(master_user)
	update_dict = correct_update_for_work_with_need_materials()
	response = patch_data(user, 'work_update', data=update_dict, id=work.id)
	assert response.status_code == rest_status.HTTP_403_FORBIDDEN
	response = patch_data(master_user, 'work_update', data=update_dict, id=work.id+1)
	assert response.status_code == rest_status.HTTP_400_BAD_REQUEST
	update_dict = incorrect_update_for_work_with_need_materials()
	response = patch_data(master_user, 'work_update', data=update_dict, id=work.id)
	assert response.status_code == rest_status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_destroy_work_ok(master_user):
	work = create_work_with_need_materials(master_user)
	response = del_response(master_user, 'work_remove', id=work.id)
	assert response.status_code == rest_status.HTTP_204_NO_CONTENT
	assert Work.active_objects.count() == 0


@pytest.mark.django_db
def test_destroy_work_fails(master_user, user):
	work = create_work_with_need_materials(master_user)
	response = del_response(user, 'work_remove', id=work.id)
	assert response.status_code == rest_status.HTTP_403_FORBIDDEN
	assert Work.active_objects.count() == 1
	response = del_response(master_user, 'work_remove', id=work.id + 1)
	assert response.status_code == rest_status.HTTP_400_BAD_REQUEST
	assert Work.active_objects.count() == 1

import pytest
from rest_framework import status as rest_status

from diploma.apps.user.models import MasterUser
from diploma.tests.test_apps.test_user.constants import TEST_USER_NAME
from diploma.tests.test_apps.test_user.utils import get_base_update_user_dict, get_base_update_user_incorrect_dict, \
	get_admin_update_user_dict
from diploma.tests.utils import patch_data, del_response


@pytest.mark.django_db
def test_update_user_ok(user):
	update_dict = get_base_update_user_dict()
	response = patch_data(user, 'user_itself_update', data=update_dict)
	assert response.status_code == rest_status.HTTP_200_OK
	assert MasterUser.objects.first().first_name == TEST_USER_NAME


@pytest.mark.django_db
def test_update_user_fail(user):
	update_dict = get_base_update_user_incorrect_dict()
	patch_data(user, 'user_itself_update', data=update_dict)
	assert not MasterUser.objects.first().is_staff


@pytest.mark.django_db
def test_update_user_admin_ok(user, admin_user):
	update_dict = get_admin_update_user_dict()
	response = patch_data(admin_user, 'user_admin_update', data=update_dict, id=user.id)
	assert response.status_code == rest_status.HTTP_200_OK
	user.refresh_from_db()
	assert user.is_staff


@pytest.mark.django_db
def test_update_user_admin_fail(user, admin_user):
	update_dict = get_admin_update_user_dict()
	response = patch_data(user, 'user_admin_update', data=update_dict, id=user.id)
	assert response.status_code == rest_status.HTTP_400_BAD_REQUEST
	response = patch_data(admin_user, 'user_admin_update', data=update_dict, id=admin_user.id)
	assert response.status_code == rest_status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_delete_user_ok(user, admin_user):
	response = del_response(admin_user, 'user_delete', id=user.id)
	assert response.status_code == rest_status.HTTP_204_NO_CONTENT
	user.refresh_from_db()
	assert user.is_deleted


@pytest.mark.django_db
def test_delete_user_fails(user, admin_user):
	response = del_response(admin_user, 'user_delete', id=admin_user.id)
	assert response.status_code == rest_status.HTTP_400_BAD_REQUEST
	response = del_response(user, 'user_delete', id=admin_user.id)
	assert response.status_code == rest_status.HTTP_400_BAD_REQUEST

import pytest

from diploma.apps.user.factories import UserFactory


@pytest.fixture
def user():
	return UserFactory(is_active=True)


@pytest.fixture
def second_user():
	return UserFactory()


@pytest.fixture
def blocked_user():
	return UserFactory(is_deleted=True)


@pytest.fixture
def admin_user():
	return UserFactory(is_staff=True)


@pytest.fixture
def master_user():
	return UserFactory(is_master=True)

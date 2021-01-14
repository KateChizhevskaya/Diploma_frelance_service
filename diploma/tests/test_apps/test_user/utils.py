from diploma.tests.test_apps.test_user.constants import TEST_USER_NAME


def get_base_update_user_dict():
	return {
		'first_name': TEST_USER_NAME
	}


def get_base_update_user_incorrect_dict():
	return {
		'first_name': TEST_USER_NAME,
		'is_staff': True
	}


def get_admin_update_user_dict():
	return {
		'is_staff': True
	}


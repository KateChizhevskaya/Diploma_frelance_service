from typing import AnyStr, Dict

from rest_framework import reverse as rest_reverse
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient

from diploma.apps.user.models import MasterUser


def prepare_request(user: MasterUser = None, url: AnyStr = 'https/', **kwargs):
	rest_request_factory = APIClient()
	if user:
		rest_request_factory.force_authenticate(user)
	return rest_reverse.reverse(url, kwargs=kwargs), rest_request_factory


def get_response(user: MasterUser, url: AnyStr, data: Dict = None, **kwargs) -> Response:
	url, rest_request_factory = prepare_request(user, url, **kwargs)
	return rest_request_factory.get(url, data=data)


def del_response(user: MasterUser, url: AnyStr, data: Dict = None, **kwargs) -> Response:
	url, rest_request_factory = prepare_request(user, url, **kwargs)
	return rest_request_factory.delete(url, data=data)


def post_data(user, url, data=None, **kwargs):
	if kwargs.get('format'):
		format = kwargs.get('format')
		kwargs.pop('format')
		url, rest_request_factory = prepare_request(user, url, **kwargs)
		return rest_request_factory.post(url, data=data, format=format)
	url, rest_request_factory = prepare_request(user, url, **kwargs)
	return rest_request_factory.post(url, data=data)


def put_data(user, url, data=None, **kwargs):
	url, rest_request_factory = prepare_request(user, url, **kwargs)
	return rest_request_factory.put(url, data=data)


def patch_data(user, url, data=None, **kwargs):
	url, rest_request_factory = prepare_request(user, url, **kwargs)
	return rest_request_factory.patch(url, data=data)
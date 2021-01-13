import random

import pytest
from rest_framework import status as rest_status

from diploma.apps.reactions.factories import ReviewFactory
from diploma.apps.reactions.models import Review
from diploma.apps.works.models import Work
from diploma.tests.test_apps.test_reaction.utils import create_order_for_answer, get_base_review, \
	create_incorrect_order_for_answer, get_base_review_update
from diploma.tests.utils import post_data, patch_data, del_response


@pytest.mark.django_db
def test_create_review_ok(user, master_user):
	work = create_order_for_answer(user, master_user)
	rating = random.randint(1, 4)
	create_dict = get_base_review(work, rating)
	response = post_data(user, 'review_create', data=create_dict)
	assert response.status_code == rest_status.HTTP_201_CREATED
	assert Review.objects.count() == 1
	assert Work.objects.first().rating == rating


@pytest.mark.django_db
def test_create_review_fail(user, master_user):
	work = create_order_for_answer(user, master_user)
	rating = random.randint(1, 4)
	create_dict = get_base_review(work, rating)
	create_dict.pop('rating')
	response = post_data(user, 'review_create', data=create_dict)
	assert response.status_code == rest_status.HTTP_400_BAD_REQUEST
	work = create_incorrect_order_for_answer(user, master_user)
	create_dict = get_base_review(work, rating)
	response = post_data(user, 'review_create', data=create_dict)
	assert response.status_code == rest_status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_update_review_ok(user, master_user):
	work = create_order_for_answer(user, master_user)
	first_rating = random.randint(1, 4)
	review = ReviewFactory(work=work, rating=first_rating, user=user)
	second_rating = random.randint(1, 4)
	work.rating = first_rating
	work.save()
	update_dict = get_base_review_update(second_rating)
	response = patch_data(user, 'review_update_destroy', data=update_dict, id=review.id)
	assert response.status_code == rest_status.HTTP_200_OK
	assert Work.objects.first().rating == second_rating


@pytest.mark.django_db
def test_update_review_fail(user, master_user):
	work = create_order_for_answer(user, master_user)
	first_rating = random.randint(1, 4)
	review = ReviewFactory(work=work, rating=first_rating, user=user)
	second_rating = random.randint(6, 10)
	work.rating = first_rating
	work.save()
	update_dict = get_base_review_update(second_rating)
	response = patch_data(user, 'review_update_destroy', data=update_dict, id=review.id)
	assert response.status_code == rest_status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_delete_review_ok(user, master_user):
	work = create_order_for_answer(user, master_user)
	first_rating = random.randint(1, 4)
	ReviewFactory(work=work, rating=first_rating, user=user)
	second_rating = random.randint(1, 4)
	review_2 = ReviewFactory(work=work, rating=second_rating, user=user)
	work.rating = (first_rating + second_rating) / 2
	work.save()
	response = del_response(user, 'review_update_destroy', id=review_2.id)
	assert response.status_code == rest_status.HTTP_204_NO_CONTENT
	assert Review.objects.count() == 1
	assert Work.objects.first().rating == first_rating


@pytest.mark.django_db
def test_update_review_ok(user, master_user):
	work = create_order_for_answer(user, master_user)
	first_rating = random.randint(1, 4)
	review = ReviewFactory(work=work, rating=first_rating, user=user)
	response = del_response(master_user, 'review_update_destroy', id=review.id)
	assert response.status_code == rest_status.HTTP_400_BAD_REQUEST

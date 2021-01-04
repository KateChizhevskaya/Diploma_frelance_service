from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError

from diploma.apps.reactions.models import Review
from diploma.apps.reactions.serializers import AddReviewSerializer, UpdateReviewSerializer


class AddReviewView(generics.CreateAPIView):
	permission_classes = (permissions.IsAuthenticated, )
	serializer_class = AddReviewSerializer


class UpdateReviewView(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (permissions.IsAuthenticated, )
	serializer_class = UpdateReviewSerializer

	def get_object(self):
		try:
			return Review.objects.get(id=self.kwargs['id'], user=self.request.user)
		except Review.DoesNotExist:
			raise ValidationError(
				'You can not update that order'
			)

	def recalculate_work_raiting(self, instance):
		work = instance.work
		work_reviews = list(filter(
			lambda rating: rating is not None,
			Review.objects.filter(work=work).values_list('rating', flat=True)
		))
		work.rating = sum(map(lambda str_num: int(str_num), work_reviews)) / len(work_reviews)
		work.save(update_fields=('rating', ))

	def perform_destroy(self, instance):
		super(UpdateReviewView, self).perform_destroy(instance)
		self.recalculate_work_raiting(instance)

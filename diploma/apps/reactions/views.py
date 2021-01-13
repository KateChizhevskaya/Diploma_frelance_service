from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError

from diploma.apps.reactions.models import Review, Complaint
from diploma.apps.reactions.serializers import AddReviewSerializer, UpdateReviewSerializer, AddComplaintSerializer, \
	ListComplaintSerializer, RetrieveComplaintSerializer, ReviewListSerializer, ReviewShowSerializer


class AddComplaintView(generics.CreateAPIView):
	permission_classes = (permissions.IsAuthenticated, )
	serializer_class = AddComplaintSerializer


class ListComplaintView(generics.ListAPIView):
	permissions = (permissions.IsAuthenticated, permissions.IsAdminUser, )
	serializer_class = ListComplaintSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['status', ]
	queryset = Complaint.objects.all()


class RetrieveComplaintView(generics.RetrieveAPIView):
	permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser,)
	lookup_field = 'id'
	serializer_class = RetrieveComplaintSerializer
	queryset = Complaint.objects.all()


class ListMyComplaintView(generics.ListAPIView):
	permissions = (permissions.IsAuthenticated, )
	serializer_class = ListComplaintSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['status', ]

	def get_queryset(self):
		if not self.request.user.is_anonymous:
			return Complaint.objects.filter(complaint_creater=self.request.user)
		else:
			raise ValidationError(
				'You need to login first'
			)


class RetrieveMyComplaintView(generics.RetrieveAPIView):
	permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser,)
	lookup_field = 'id'
	serializer_class = RetrieveComplaintSerializer

	def get_queryset(self):
		if not self.request.user.is_anonymous:
			return Complaint.objects.filter(complaint_creater=self.request.user)
		else:
			raise ValidationError(
				'You need to login first'
			)


class AddReviewView(generics.CreateAPIView):
	permission_classes = (permissions.IsAuthenticated, )
	serializer_class = AddReviewSerializer


class ListMyReviewsView(generics.ListAPIView):
	permissions = (permissions.IsAuthenticated, )
	serializer_class = ReviewListSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['rating', ]

	def get_queryset(self):
		if not self.request.user.is_anonymous:
			return Review.objects.filter(user=self.request.user)
		else:
			raise ValidationError(
				'You need to login first'
			)


class RetrieveMyReviewView(generics.RetrieveAPIView):
	permission_classes = (permissions.IsAuthenticated,)
	lookup_field = 'id'
	serializer_class = ReviewShowSerializer

	def get_queryset(self):
		if not self.request.user.is_anonymous:
			return Review.objects.filter(user=self.request.user)
		else:
			raise ValidationError(
				'You need to login first'
			)


class UpdateDeleteReviewView(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (permissions.IsAuthenticated, )
	serializer_class = UpdateReviewSerializer

	def get_object(self):
		if not self.request.user.is_anonymous:
			try:
				return Review.objects.get(id=self.kwargs['id'], user=self.request.user)
			except Review.DoesNotExist:
				raise ValidationError(
					'You can not update that order'
				)
		else:
			raise ValidationError(
				'You need to login first'
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
		super(UpdateDeleteReviewView, self).perform_destroy(instance)
		self.recalculate_work_raiting(instance)

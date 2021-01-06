from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from diploma.apps.order.constants import ACTIVE_STATUS
from diploma.apps.order.models import WorkOrder
from diploma.apps.reactions.serializers import ReviewShowSerializer
from diploma.apps.tasks.mail_sending import send_mails_to_many_users
from diploma.apps.user.serializers import ShowUsersSerializer
from diploma.apps.works.constants import MaterialsNeed, WORK_TEXT_START, WORK_CHANGE_TEXT_END, WORK_CHANGE_HEADER
from diploma.apps.works.models import Work


class UpdateWorkSerializer(ModelSerializer):
	class Meta:
		model = Work
		fields = [
			'comment',
			'placement',
			'nim_cost_with_materials',
			'nim_cost_without_materials',
			'need_materials',
		]

	def check_for_not_attr(self, instance, validated_data, attr, value):
		return not getattr(instance, attr) == value and not validated_data.get(attr) == value

	def check_for_attr_existing(self, instance, validated_data, attr):
		return getattr(instance, attr) or validated_data.get(attr)

	def validate_price_change(self, instance, validated_data):
		if validated_data.get('nim_cost_with_materials') or validated_data.get('nim_cost_without_materials') \
				and self.check_for_not_attr(instance, validated_data, 'need_materials', MaterialsNeed.BOTH):
			if validated_data.get('nim_cost_with_materials') and \
					self.check_for_not_attr(instance, validated_data, 'need_materials', MaterialsNeed.YES):
				raise serializers.ValidationError(
					'You need to enter only price without materials'
				)
			elif validated_data.get('nim_cost_without_materials') and \
					self.check_for_not_attr(instance, validated_data, 'need_materials', MaterialsNeed.NO):
				raise serializers.ValidationError(
					'You need to enter only price with materials'
				)

	def validate_need_materials_change(self, instance, validated_data):
		if validated_data.get('need_materials') and validated_data.get('need_materials') != instance.need_materials:
			if validated_data.get('need_materials') == MaterialsNeed.BOTH and \
					(
							not self.check_for_attr_existing(instance, validated_data, 'nim_cost_without_materials')
							or not self.check_for_attr_existing(instance, validated_data, 'nim_cost_with_materials')
					):
				raise serializers.ValidationError(
					'You need to enter both price with and without materials or do not change need_materials'
				)
			if validated_data.get('need_materials') == MaterialsNeed.YES and \
					not self.check_for_attr_existing(instance, validated_data, 'nim_cost_with_materials'):
				raise serializers.ValidationError(
					'You need to enter only price with materials or do not change need_materials'
				)
			if validated_data.get('need_materials') == MaterialsNeed.NO and \
					not self.check_for_attr_existing(instance, validated_data, 'nim_cost_without_materials'):
				raise serializers.ValidationError(
					'You need to enter only price without materials or do not change need_materials'
				)

	def change_instance_for_need_materials(self, instance):
		if instance.need_materials == MaterialsNeed.YES and instance.nim_cost_without_materials is not None:
			instance.nim_cost_without_materials = None
			instance.save(update_fields=['nim_cost_without_materials'])
		elif instance.need_materials == MaterialsNeed.NO and instance.nim_cost_with_materials is not None:
			instance.nim_cost_with_materials = None
			instance.save(update_fields=['nim_cost_with_materials'])

	def send_email(self, instance):
		text = WORK_TEXT_START + instance.name + WORK_CHANGE_TEXT_END
		emails = filter(
			lambda one_order: one_order is not None,
			(order.customer_email for order in WorkOrder.objects.filter(work__id=instance.id, status__in=ACTIVE_STATUS))
		)
		send_mails_to_many_users(WORK_CHANGE_HEADER, text, users=None, users_mails=emails)

	def update(self, instance, validated_data):
		self.validate_price_change(instance, validated_data)
		instance = super(UpdateWorkSerializer, self).update(instance, validated_data)
		self.change_instance_for_need_materials(instance)
		instance.refresh_from_db()
		self.send_email(instance)
		return instance


class ListWorkSerializer(ModelSerializer):
	worker = ShowUsersSerializer(read_only=True)

	class Meta:
		model = Work
		fields = [
			'id',
			'comment',
			'placement',
			'name',
			'nim_cost_with_materials',
			'nim_cost_without_materials',
			'need_materials',
			'worker'
		]


class RetrieveWorkSerializer(ModelSerializer):
	reviews = ReviewShowSerializer(read_only=True, many=True)
	worker = ShowUsersSerializer(read_only=True)

	class Meta:
		model = Work
		fields = [
			'id',
			'rating',
			'comment',
			'placement',
			'name',
			'nim_cost_with_materials',
			'nim_cost_without_materials',
			'need_materials',
			'worker',
			'reviews'
		]


class CreateWorkSerializer(ModelSerializer):
	class Meta:
		model = Work
		fields = [
			'comment',
			'placement',
			'name',
			'nim_cost_with_materials',
			'nim_cost_without_materials',
			'need_materials'
		]
		extra_kwargs = {
			'comment': {
				'required': False,
				'allow_blank': False,
			},
			'placement': {
				'required': False,
				'allow_blank': False,
			},
			'name': {
				'required': True,
				'allow_blank': False,
			},
			'nim_cost_with_materials': {
				'required': False,
			},
			'nim_cost_without_materials': {
				'required': False,
			},
			'need_materials': {
				'required': False,
				'allow_blank': False,
			}
		}

	def _validate_price(self, attrs):
		if attrs.get('need_materials'):
			if attrs.get('need_materials') == MaterialsNeed.NO:
				if not (attrs.get('nim_cost_without_materials') and not attrs.get('nim_cost_with_materials')):
					raise serializers.ValidationError(
						'You need to enter only price without materials'
					)
			elif attrs.get('need_materials') == MaterialsNeed.YES:
				if not (not attrs.get('nim_cost_without_materials') and attrs.get('nim_cost_with_materials')):
					raise serializers.ValidationError(
						'You need to enter only price with materials'
					)
			else:
				if not (attrs.get('nim_cost_without_materials') and attrs.get('nim_cost_with_materials')):
					raise serializers.ValidationError(
						'You need to enter both prices'
					)
		else:
			if not (attrs.get('nim_cost_without_materials') and not attrs.get('nim_cost_with_materials')):
				raise serializers.ValidationError(
					'You need to enter only price without materials'
				)

	def validate(self, attrs):
		self._validate_price(attrs)
		return attrs

	def create(self, validated_data):
		validated_data['worker'] = self.context['request'].user
		return Work.objects.create(**validated_data)

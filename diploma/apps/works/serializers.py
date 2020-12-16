from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from diploma.apps.works.constants import MaterialsNeed
from diploma.apps.works.models import Work


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
				if not(attrs.get('nim_cost_without_materials') and not attrs.get('nim_cost_with_materials')):
					raise serializers.ValidationError(
						'You need to enter only price without materials'
					)
			elif attrs.get('need_materials') == MaterialsNeed.YES:
				if not(not attrs.get('nim_cost_without_materials') and attrs.get('nim_cost_with_materials')):
					raise serializers.ValidationError(
						'You need to enter only price with materials'
					)
			else:
				if not(attrs.get('nim_cost_without_materials') and attrs.get('nim_cost_with_materials')):
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

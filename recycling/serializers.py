from rest_framework import serializers
from recycling.models import (
    RecyclingLocation,
    RecyclableMaterialCategory
)
from marketplace.models import Consumer

class RecyclingLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecyclingLocation
        fields = [
            'id',
            'name',
            'address',
            'contact',
            'latitude',
            'longitude'
        ]


class RecyclableMaterialReceptionSerializer(serializers.Serializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset = RecyclableMaterialCategory.objects.all(),
        source='material_category_obj'
    )
    name = serializers.CharField()
    description = serializers.CharField()
    quantity_gram = serializers.IntegerField(min_value=1)
    consumer_id = serializers.PrimaryKeyRelatedField(
        queryset = Consumer.objects.all(),
        source='consumer_obj',
        required=False
    )

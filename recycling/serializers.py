from rest_framework import serializers
from recycling.models import (
    RecyclingLocation,
    RecyclableMaterialCategory
)
from marketplace.models import Consumer
from django.contrib.auth import get_user_model

User = get_user_model()

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


class RecyclableMaterialCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RecyclableMaterialCategory
        fields = ["id", "name"]


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


class ConsumerSummarySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")

    class Meta:
        model = Consumer
        fields = ["pk", "username"]

from rest_framework import serializers
from recycling.models import RecyclingLocation

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

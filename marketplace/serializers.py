from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Consumer,
    Company,
    ProductCategory,
    Product,
    ConsumerSavedProduct,
    Coupon
)
# auxiliary library for CPF/CNPJ validation
from validate_docbr import CPF
import re

User = get_user_model()

class ConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumer
        fields = "__all__"

class ConsumerRegistrationSerializer(serializers.ModelSerializer):
    # Embedded user fields directly in the serializer
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True,
                                     style={"input_type": "password"})
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)

    class Meta:
        model = Consumer
        fields = [
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "cpf",
            "phone",
            "address"
        ]

    def validate_cpf(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError("Invalid CPF.")
        # Regular expression for the format xxx.xxx.xxx-xx
        regex_cpf = r'^\d{3}\.\d{3}\.\d{3}-\d{2}$'
        if not re.match(regex_cpf, value):
            raise serializers.ValidationError("Invalid CPF.")
        cpf = CPF()
        if not cpf.validate(value):
            raise serializers.ValidationError("Invalid CPF.")
        return value

    def create(self, validated_data):
        # Extracts user data
        username = validated_data.pop("username")
        email = validated_data.pop("email")
        password = validated_data.pop("password")
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        
        user_data = {
            "username": username,
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "role": User.UserRole.CONSUMER
        }

        # Creates the user with the CONSUMER role
        user = User.objects.create_user(**user_data)

        # Creates the associated consumer
        consumer = Consumer.objects.create(user=user, **validated_data)

        return consumer

class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    company = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price_cents',
            'quantity',
            'purchase_contact',
            'category',
            'company',
            'is_sustainable',
            'created_at',
        ]

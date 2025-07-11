from rest_framework import serializers
from django.contrib.auth import get_user_model
from marketplace.models import (
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

class ConsumerRetrieveSerializer(serializers.ModelSerializer):
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
        # if not isinstance(value, str):
        #     raise serializers.ValidationError("Invalid CPF.")
        # # Regular expression for the format xxx.xxx.xxx-xx
        # regex_cpf = r'^\d{3}\.\d{3}\.\d{3}-\d{2}$'
        # if not re.match(regex_cpf, value):
        #     raise serializers.ValidationError("Invalid CPF.")
        # cpf = CPF()
        # if not cpf.validate(value):
        #     raise serializers.ValidationError("Invalid CPF.")
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

# NOTE: Deprecated Serializer
# class ProductSerializer(serializers.ModelSerializer):
#     category = serializers.StringRelatedField()
#     company = serializers.StringRelatedField()
    
#     class Meta:
#         model = Product
#         fields = "__all__"

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price_cents',
            'image',
        ]

class ProductRetrieveSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)
    company = serializers.CharField(source='company.user.get_full_name',
                                    read_only=True)
    # Field to indicate whether the product is saved by the logged in consumer
    is_saved_by_consumer = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description',
                  'price_cents', 'quantity', 'purchase_contact',
                  'category', 'company', 'is_sustainable',
                  'created_at', 'is_saved_by_consumer', 'image',]        

    def get_is_saved_by_consumer(self, obj):
        # self.context['request'] contains the view's request object
        request = self.context.get('request')

        # If there is no request or the user is not authenticated, or
        # is not a consumer, returns False
        if not request or not request.user.is_authenticated:
            return None

        # Checks if the authenticated user has an associated Consumer object
        try:
            consumer = request.user.consumer
        except Consumer.DoesNotExist:
            return None # Authenticated user is not a consumer

        # Checks if a record exists in ConsumerSavedProduct
        # for this product and this consumer
        return ConsumerSavedProduct.objects.filter(
            consumer=consumer,
            product=obj # obj is the current Product instance being serialized
        ).exists()

class ConsumerSavedProductListSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()

    class Meta:
        model = ConsumerSavedProduct
        fields = ['id', 'product', 'saved_at']

class ConsumerSavedProductCreateSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product'
    )
    
    class Meta:
        model = ConsumerSavedProduct
        fields = ['id', 'product_id', 'saved_at']
        read_only_fields = ['id', 'saved_at']

class ProductCreateSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductCategory.objects.all(),
        source='category'
    )

    # Optional image field, allowing null values
    image = serializers.ImageField(required=False,
                                   allow_null=True)

    class Meta:
        model = Product
        fields = [
            'category_id',
            'name',
            'description',
            'price_cents',
            'quantity',
            'purchase_contact',
            'image',
        ]

class CouponGenerationSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(is_active=True),
        source='product_obj'
    )
    green_credit_amount = serializers.IntegerField(min_value=1)

class CouponListSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        source='product',
        read_only=True
    )

    class Meta:
        model = Coupon
        fields = [
            'id',
            'coupon_code',
            'discount_value_cents',
            'generated_at',
            'is_valid',
            'product_id',
        ]

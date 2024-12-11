from rest_framework import serializers
from django.contrib.auth.models import User
from v1.models import Customer
from v1.models import Admin
from django.utils.crypto import get_random_string

from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_username(self, value):
        """Ensure the username is unique"""
        if User.objects.filter(username=value).exists():
            raise ValidationError("This username is already taken.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user



from django.core.exceptions import ValidationError

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    email = serializers.EmailField(required=True)  # Email is now a field in CustomerSerializer

    class Meta:
        model = Customer
        fields = [
            'user', 'email', 'first_name', 'last_name', 'phone_number', 
            'address', 'subscribed_to_promotions', 'account_state'
        ]

    def validate_email(self, value):
        # Ensure that the email is unique for Customer
        if Customer.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def validate_username(self, value):
        # Ensure the username is unique for User
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def create(self, validated_data):
        # Separate user data from customer data
        user_data = validated_data.pop('user')
        password = user_data.pop('password')

        # Create the user and set password
        user = User.objects.create(**user_data)
        user.set_password(password)
        user.save()

        # Generate a random verification token for email verification
        verification_token = get_random_string(32)

        # Create the customer object and save it
        customer = Customer.objects.create(
            user=user,
            verification_token=verification_token,
            **validated_data
        )

        return customer

    
class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Admin
        fields = ['user', 'email', 'first_name', 'last_name']
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password')
        user = User.objects.create(**user_data)
        user.set_password(password)
        user.save()
        admin = Admin.objects.create(
            user=user,
            **validated_data
        )
        return admin

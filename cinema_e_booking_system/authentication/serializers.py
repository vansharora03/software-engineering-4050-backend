from rest_framework import serializers
from django.contrib.auth.models import User
from v1.models import Customer
from v1.models import Admin
from django.utils.crypto import get_random_string

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = [
            'user', 'email', 'first_name', 'last_name', 'phone_number', 
            'address', 'subscribed_to_promotions', 'account_state'
        ]

    def create(self, validated_data):
    
        user_data = validated_data.pop('user')
        password = user_data.pop('password')

        user = User.objects.create(**user_data)
        user.set_password(password)
        user.save()

        # Generate a random verification token for email verification
        verification_token = get_random_string(32)

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

from rest_framework import serializers
from django.contrib.auth.models import User
from v1.models import Customer

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
        fields = ['user', 'email', 'first_name', 'last_name', 'phone_number', 'address', 'subscribed_to_promotions', 'account_state']

    def create(self, validated_data):

        user_data = validated_data.pop('user')
        password = user_data.pop('password')

        user = User.objects.create(**user_data)
        user.set_password(password)
        user.save()

        customer = Customer.objects.create(user=user, **validated_data)
        return customer

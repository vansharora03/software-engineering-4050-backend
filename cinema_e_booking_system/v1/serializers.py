from rest_framework import serializers
from .models import Movie, PaymentCard

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"

class PaymentCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentCard
        fields = ["cardholder_name", "billing_address", "expiry_date"]

from rest_framework import serializers
from .models import Movie, PaymentCard, Showtime, Seat, Booking, TicketType, Ticket, Promotion, Showroom

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"

class PaymentCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentCard
        fields = "__all__"

class ShowtimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Showtime
        fields = "__all__"

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = "__all__"

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"

class TicketTypeSerializer(serializers.ModelSerializer):
    showtime = ShowtimeSerializer()
    class Meta:
        model = TicketType
        fields = "__all__"

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"  

class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = "__all__"

class ShowroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Showroom
        fields = "__all__"
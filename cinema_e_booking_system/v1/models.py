from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    subscribed_to_promotions = models.BooleanField(default=False)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    verification_token = models.CharField(max_length=32, blank=True, null=True)
    # Enum
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    SUSPENDED = 'suspended'
    ACCOUNT_STATE_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
        (SUSPENDED, 'Suspended'),
    ]
    account_state = models.CharField(
        max_length=10,
        choices=ACCOUNT_STATE_CHOICES,
        default=ACTIVE,
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    class Meta:
        db_table = "Customer"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
import hashlib

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_title = models.CharField(max_length=255, null=True, blank=True)
    seat_number = models.CharField(max_length=10, null=True, blank=True)
    booking_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    promotion = models.ForeignKey('Promotion', null=True, blank=True, on_delete=models.SET_NULL)
    payment_card = models.ForeignKey('PaymentCard', on_delete=models.CASCADE)

    def __str__(self):
        return f'Booking for {self.movie_title} by {self.user.username}'

    class Meta:
        db_table = "Booking"
        ordering = ['-booking_date']

class Promotion(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

    def is_active(self):
        from django.utils import timezone
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date
    

import hashlib

class PaymentCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cardholder_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=19)  # Add this field to store the raw card number
    hashed_card_number = models.CharField(max_length=64)
    expiry_date = models.DateField()
    billing_address = models.CharField(max_length=255)
    last_four_digits = models.CharField(max_length=4, blank=True, null=True)  # Store the last 4 digits

    class Meta:
        db_table = 'PaymentCard'

    def hash_card_number(self, card_number):
        """Hashes the card number using SHA256."""
        return hashlib.sha256(card_number.encode()).hexdigest()

    def save(self, *args, **kwargs):
        # Hash the card number before saving
        if hasattr(self, 'card_number') and self.card_number:
            # Hash the card number and store it
            self.hashed_card_number = self.hash_card_number(self.card_number)
            # Extract the last four digits from the raw card number
            self.last_four_digits = self.card_number[-4:]  # Get the last 4 digits
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.cardholder_name} ending in {self.last_four_digits}'

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    class Meta:
        db_table = "Admin"
        verbose_name_plural = 'Admins'

    def __str__(self):
        return self.user.username
class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    trailer_link = models.CharField(max_length=500)
    img_link = models.CharField(max_length=500)
    duration = models.PositiveIntegerField() 
    release_date = models.DateTimeField(editable=True)

    class Meta:
        db_table = 'Movie'
        verbose_name_plural = 'Movies'
    
    def __str__(self):
        return self.title

class Showroom(models.Model):
    name = models.CharField(max_length=100)
    seat_count = models.PositiveIntegerField(null=True, blank=True)
    class Meta:
        db_table = 'Showroom'
        verbose_name_plural = 'Showrooms'
    
    def __str__(self):
        return self.name

class Seat(models.Model):
    number = models.PositiveIntegerField()
    showroom = models.ForeignKey(Showroom, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "Seat"

class Showtime(models.Model):
    time = models.DateTimeField(editable=True)
    duration = models.PositiveIntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    showroom = models.ForeignKey(Showroom, on_delete=models.CASCADE)

    class Meta:
        db_table = "Showtime"

class TicketType(models.Model):
    name = models.CharField(max_length=50) 
    price = models.DecimalField(max_digits=6, decimal_places=2)  

    class Meta:
        db_table = 'TicketType'
        verbose_name_plural = 'TicketTypes'

    def __str__(self):
        return f'{self.name} - {self.price}'


class Ticket(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)  
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE) 
    seat_number = models.CharField(max_length=10)
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'Ticket'
        verbose_name_plural = 'Tickets'

    def __str__(self):
        return f'Ticket for {self.booking.movie_title} ({self.ticket_type.name})'

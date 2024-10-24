from django.db import models
from django.contrib.auth.models import User

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_title = models.CharField(max_length=255)
    show_time = models.DateTimeField()
    seat_number = models.CharField(max_length=10)
    booking_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    promotion = models.ForeignKey('Promotion', null=True, blank=True, on_delete=models.SET_NULL)  # Nullable ForeignKey
    payment_card = models.ForeignKey('PaymentCard', on_delete=models.CASCADE)

    def __str__(self):
        return f'Booking for {self.movie_title} by {self.user.username}'

    class Meta:
        ordering = ['-booking_date']

class Promotion(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

    def is_active(self):
        from django.utils import timezone
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date


class PaymentCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cardholder_name = models.CharField(max_length=255)
    last_four_digits = models.CharField(max_length=4)
    expiry_date = models.DateField()
    card_type = models.CharField(max_length=50)  # e.g., Visa, MasterCard

    def __str__(self):
        return f'{self.card_type} ending in {self.last_four_digits}'
# Create your models here.

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

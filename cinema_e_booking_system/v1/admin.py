# admin.py
from django.contrib import admin
from .models import Booking, Promotion, PaymentCard

admin.site.register(Booking)
admin.site.register(Promotion)
admin.site.register(PaymentCard)



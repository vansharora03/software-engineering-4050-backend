# admin.py
from django.contrib import admin
from .models import Booking, Promotion, PaymentCard

admin.site.register(Booking)
admin.site.register(Promotion)
admin.site.register(PaymentCard)

from django.contrib import admin
from .models import TheatreLoggingSystem

@admin.register(TheatreLoggingSystem)
class TheatreLoggingSystemAdmin(admin.ModelAdmin):
    list_display = ('date', 'child_purchases', 'adult_purchases', 'senior_purchases', 'total_purchases')
    ordering = ('-date',)
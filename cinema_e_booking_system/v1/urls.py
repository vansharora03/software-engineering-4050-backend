from . import views
from django.urls import path

urlpatterns = [
    path("hello", views.hello, name="hello"),
    path("movies", views.movies, name="movies"),
    path("movies/<int:movie_id>", views.movies, name="getMovie"),
     # Booking URLs
    path("bookings", views.booking_list, name="booking_list"),
    path("bookings/create", views.booking_create, name="booking_create"),
    path("bookings/<int:id>", views.booking_detail, name="booking_detail"),
    path("bookings/<int:id>/update", views.booking_update, name="booking_update"),
    path("bookings/<int:id>/delete", views.booking_delete, name="booking_delete"),
    # Promotion URLs
    path("promotions", views.promotion_list, name="promotion_list"),
    path("promotions/create", views.promotion_create, name="promotion_create"),
    path("promotions/<int:id>", views.promotion_detail, name="promotion_detail"),
    path("promotions/<int:id>/update", views.promotion_update, name="promotion_update"),
    path("promotions/<int:id>/delete", views.promotion_delete, name="promotion_delete"),
    # PaymentCard URLs
    path("payment-cards", views.payment_card_list, name="payment_card_list"),
    path("payment-cards/add", views.payment_card_add, name="payment_card_add"),
    path("payment-cards/<int:id>", views.payment_card_detail, name="payment_card_detail"),
    path("payment-cards/<int:id>/update", views.payment_card_update, name="payment_card_update"),
    path("payment-cards/<int:id>/delete", views.payment_card_delete, name="payment_card_delete"),
]


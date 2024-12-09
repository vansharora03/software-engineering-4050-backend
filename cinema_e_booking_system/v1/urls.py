from . import views
from django.urls import path

urlpatterns = [
    path("hello", views.hello, name="hello"),
    path("movies", views.movies, name="movies"),
    path("movies/<int:movie_id>", views.movies, name="getMovie"),
    path("movies/<int:movie_id>/showtimes", views.showtimes, name="showtimes"),
    path("showtimes/movies/<int:movie_id>", views.add_showtime, name="add_showtime"),
    path("showtimes/<int:showtime_id>/seats/<int:seat_number>", views.is_seat_available, name="is_seat_available"),
    path("seats", views.add_seat, name="add_seat"),
    path("tickets", views.add_ticket, name="add_ticket"),
    path("tickets/<int:ticket_id>", views.get_ticket, name="get_ticket"),
    path("bookings/<int:id>/tickets", views.get_tickets, name="get_tickets"),
     # Booking URLs
    path("bookings/<int:id>", views.get_booking, name="get_booking"),
    path("bookings", views.add_booking, name="add_booking"),
    path("bookings/get", views.get_bookings, name="get_bookings"),
    # Promotion URLs
    path("promotions", views.promotion_list, name="promotion_list"),
    path("promotions/create", views.promotion_create, name="promotion_create"),
    path("promotions/<int:id>", views.promotion_detail, name="promotion_detail"),
    path("promotions/<int:id>/update", views.promotion_update, name="promotion_update"),
    path("promotions/<int:id>/delete", views.promotion_delete, name="promotion_delete"),
    # PaymentCard URLs
    path("payment-cards", views.payment_card_list, name="payment_card_list"),
    path("payment-cards/add", views.payment_card_add, name="payment_card_add"),
    path("payment-cards/<int:id>/update", views.payment_card_update, name="payment_card_update"),
    path("payment-cards/delete", views.payment_card_delete, name="payment_card_delete"),
]


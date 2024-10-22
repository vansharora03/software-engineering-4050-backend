from . import views
from django.urls import path

urlpatterns = [
    path("hello", views.hello, name="hello"),
    path("movies", views.movies, name="movies"),
    path("movies/<int:movie_id>", views.movies, name="getMovie")
]
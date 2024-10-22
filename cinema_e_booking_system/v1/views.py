from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import MovieForm
from .models import Movie
from .serializers import MovieSerializer

def hello(request: HttpRequest):
    return HttpResponse("Hello!")

def addMovie(request: HttpRequest):
    form = MovieForm(request.POST)
    if form.is_valid():
        movie = form.save()
        return JsonResponse({'movie': MovieSerializer(movie).data}, status=201)
    else:
        return JsonResponse({'errors': form.errors}, status=400)


@csrf_exempt
def movies(request: HttpRequest, movie_id=-1):
    if request.method == "POST":
        return addMovie(request)
    elif request.method == "GET" and movie_id == -1:
        movies = Movie.objects.all()
        return JsonResponse({'movies': MovieSerializer(movies, many=True).data}, status=200)
    elif request.method == "GET":
        movie = get_object_or_404(Movie, id=movie_id)
        return JsonResponse({'movie': MovieSerializer(movie).data}, status=200)
    else:
        return HttpResponse("Not handled yet")



# Create your views here.

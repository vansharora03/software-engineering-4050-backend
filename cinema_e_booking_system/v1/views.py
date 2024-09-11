from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

def hello(request: HttpRequest):
    return HttpResponse("Hello!")

# Create your views here.

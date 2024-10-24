from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import MovieForm
from .models import Movie
from .serializers import MovieSerializer
from .models import Booking, Promotion, PaymentCard

# Create your views here.

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


# Booking Views
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})

def booking_create(request):
    return render(request, 'bookings/booking_form.html')

def booking_detail(request, id):
    booking = get_object_or_404(Booking, id=id, user=request.user)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})

def booking_update(request, id):
    return render(request, 'bookings/booking_form.html')

def booking_delete(request, id):
    booking = get_object_or_404(Booking, id=id, user=request.user)
    booking.delete()
    return redirect('booking_list')


# Promotion Views
def promotion_list(request):
    promotions = Promotion.objects.filter(is_active=True)
    return render(request, 'promotions/promotion_list.html', {'promotions': promotions})

def promotion_create(request):
    return render(request, 'promotions/promotion_form.html')

def promotion_detail(request, id):
    promotion = get_object_or_404(Promotion, id=id)
    return render(request, 'promotions/promotion_detail.html', {'promotion': promotion})

def promotion_update(request, id):
    return render(request, 'promotions/promotion_form.html')

def promotion_delete(request, id):
    promotion = get_object_or_404(Promotion, id=id)
    promotion.delete()
    return redirect('promotion_list')


# PaymentCard Views
def payment_card_list(request):
    cards = PaymentCard.objects.filter(user=request.user)
    return render(request, 'payment_cards/payment_card_list.html', {'cards': cards})

def payment_card_add(request):
    return render(request, 'payment_cards/payment_card_form.html')

def payment_card_detail(request, id):
    card = get_object_or_404(PaymentCard, id=id, user=request.user)
    return render(request, 'payment_cards/payment_card_detail.html', {'card': card})

def payment_card_update(request, id):
    return render(request, 'payment_cards/payment_card_form.html')

def payment_card_delete(request, id):
    card = get_object_or_404(PaymentCard, id=id, user=request.user)
    card.delete()
    return redirect('payment_card_list')

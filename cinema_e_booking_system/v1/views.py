from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .forms import MovieForm
from .models import Movie
from .serializers import MovieSerializer, PaymentCardSerializer, ShowtimeSerializer
from .models import Booking, Promotion, PaymentCard, Ticket, TicketType, Showtime, Showroom
from django.contrib.auth.models import User
import hashlib
from datetime import datetime, time
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import json
from django.http import JsonResponse




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
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def payment_card_list(request):
    cards = PaymentCard.objects.filter(user=request.user)
    return HttpResponse(json.dumps(PaymentCardSerializer(cards, many=True).data))


@api_view(['POST'])  # Make sure this is an API view
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def payment_card_add(request):

    pc = PaymentCard.objects.create(
        user = request.user,
        cardholder_name = request.data.get("cardholder_name"),
        hashed_card_number = hashlib.sha256(request.data.get("card_number").encode()).hexdigest(),
        expiry_date = datetime.strptime(request.data.get("expiry_date"), "%Y-%m-%d"),
        billing_address = request.data.get("billing_address")
    )
    return HttpResponse(status=201)

def payment_card_detail(request, id):
    card = get_object_or_404(PaymentCard, id=id, user=request.user)
    return render(request, 'payment_cards/payment_card_detail.html', {'card': card})

def payment_card_update(request, id):
    return render(request, 'payment_cards/payment_card_form.html')

@api_view(['DELETE'])  # Make sure this is an API view
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def payment_card_delete(request, id=1):
    PaymentCard.objects.filter(user=request.user).delete()
    return redirect('payment_card_list')



# Ticket Views
def ticket_list(request):
    tickets = Ticket.objects.filter(booking__user=request.user)
    return render(request, 'tickets/ticket_list.html', {'tickets': tickets})

def ticket_create(request):
    return render(request, 'tickets/ticket_form.html')

def ticket_detail(request, id):
    ticket = get_object_or_404(Ticket, id=id, booking__user=request.user)
    return render(request, 'tickets/ticket_detail.html', {'ticket': ticket})

def ticket_update(request, id):
    return render(request, 'tickets/ticket_form.html')

def ticket_delete(request, id):
    ticket = get_object_or_404(Ticket, id=id, booking__user=request.user)
    ticket.delete()
    return redirect('ticket_list')


# TicketType Views
def ticket_type_list(request):
    ticket_types = TicketType.objects.all()
    return render(request, 'ticket_types/ticket_type_list.html', {'ticket_types': ticket_types})

def ticket_type_create(request):
    return render(request, 'ticket_types/ticket_type_form.html')

def ticket_type_detail(request, id):
    ticket_type = get_object_or_404(TicketType, id=id)
    return render(request, 'ticket_types/ticket_type_detail.html', {'ticket_type': ticket_type})

def ticket_type_update(request, id):
    return render(request, 'ticket_types/ticket_type_form.html')

def ticket_type_delete(request, id):
    ticket_type = get_object_or_404(TicketType, id=id)
    ticket_type.delete()
    return redirect('ticket_type_list')

@api_view(['GET']) 
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def showtimes(request, movie_id):
    showtimes = Showtime.objects.filter(movie__id=movie_id)
    return JsonResponse({"showtimes": ShowtimeSerializer(showtimes, many=True).data}, status=200)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_showtime(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    showroom = Showroom.objects.get(name=request.data.get("showroom"))
    showtime = Showtime.objects.create(
        time = datetime.strptime(request.data.get("time"), "%Y-%m-%d %H:%M:%S"),
        duration = request.data.get("duration"),
        movie = movie,
        showroom = showroom
    )
    return JsonResponse({"showtime": ShowtimeSerializer(showtime).data}, status=201)


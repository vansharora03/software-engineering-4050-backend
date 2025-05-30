import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .forms import MovieForm
from .models import Movie
from .serializers import MovieSerializer, PaymentCardSerializer, ShowtimeSerializer, BookingSerializer, SeatSerializer, TicketSerializer, PromotionSerializer, ShowroomSerializer
from .models import Booking, Promotion, PaymentCard, Ticket, TicketType, Showtime, Showroom, Seat
from django.contrib.auth.models import User
import hashlib
from datetime import datetime, time
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import json
from django.http import JsonResponse
from rest_framework.response import Response
from v1.factories.ticket_factory import TicketFactory
from v1.serializers import TicketSerializer

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_ticket(request):
    try:
        ticket = TicketFactory.create_ticket(
            booking_id=request.data.get("booking"),
            ticket_type_id=request.data.get("ticket_type"),
            seat_number=request.data.get("seat_number"),
            showtime_id=request.data.get("showtime"),
        )
        return Response(TicketSerializer(ticket).data, status=201)
    except ValueError as e:
        return Response({"error": str(e)}, status=400)




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
    if not request.user.is_authenticated:
        return Response({"error": "Authentication required."}, status=401)
    cards = PaymentCard.objects.filter(user=request.user)
    return JsonResponse(PaymentCardSerializer(cards, many=True).data, safe=False)

@api_view(['POST'])  # Make sure this is an API view
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def payment_card_add(request):

    pc = PaymentCard.objects.create(
        user = request.user,
        cardholder_name = request.data.get("cardholder_name"),
        hashed_card_number = hashlib.sha256(request.data.get("card_number").encode()).hexdigest(),
        expiry_date = datetime.strptime(request.data.get("expiry_date"), "%Y-%m-%d").date(),
        billing_address = request.data.get("billing_address"),
        last_four_digits = request.data.get("last_four_digits")
    )
    return JsonResponse(PaymentCardSerializer(pc).data, status=201)
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
def showtimes(request, movie_id):
    showtimes = Showtime.objects.filter(movie__id=movie_id)
    return JsonResponse({"showtimes": ShowtimeSerializer(showtimes, many=True).data}, status=200)

@api_view(['POST'])
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

@api_view(['POST'])
def add_seat(request):
    showroom = Showroom.objects.get(name=request.data.get("showroom"))
    seat = Seat.objects.create(
        number = request.data.get("number"),
        showroom = showroom
    )
    return JsonResponse({"seat": SeatSerializer(seat).data}, status=201)

@api_view(['GET'])
def get_booking(request, id):
    booking = Booking.objects.get(id=id)
    return JsonResponse({"booking": BookingSerializer(booking).data}, status=200)

from django.core.exceptions import ObjectDoesNotExist

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_booking(request):
    showtime = Showtime.objects.get(id=request.data.get("showtime"))
    card = PaymentCard.objects.get(id=request.data.get("card"))
    promotion = None
    promotion_name = request.data.get("promotion")

    if promotion_name:
        try:
            promotion = Promotion.objects.get(name=promotion_name)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Promotion not found."}, status=400)
    
    booking = Booking.objects.create(
        user=request.user,
        payment_card=card,
        promotion=promotion,
        booking_date=datetime.now()
    )
    
    return JsonResponse({"booking": BookingSerializer(booking).data}, status=201)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return JsonResponse({"bookings": BookingSerializer(bookings, many=True).data}, status=200)

@api_view(['GET'])
def get_tickets(request, id):
    booking = Booking.objects.get(id=id)
    tickets = Ticket.objects.filter(booking=booking)
    return JsonResponse({"tickets": TicketSerializer(tickets, many=True).data}, status=200)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_ticket(request):
    booking = Booking.objects.get(id=request.data.get("booking"))
    ticket_type = TicketType.objects.get(id=request.data.get("ticket_type"))
    showtime = Showtime.objects.get(id=request.data.get("showtime"))
    ticket = Ticket.objects.create(
        booking = booking,
        ticket_type = ticket_type,
        seat_number = request.data.get("seat_number"),
        showtime = showtime
    )
    return JsonResponse({"ticket": TicketSerializer(ticket).data}, status=201)

@api_view(['GET'])
def get_ticket(request, id):
    ticket = Ticket.objects.get(id=id)
    return JsonResponse({"ticket": TicketSerializer(ticket).data}, status=200)

@api_view(['GET'])
def is_seat_available(request, showtime_id, seat_number):
    showtime = Showtime.objects.get(id=showtime_id)
    return JsonResponse({"available": not Ticket.objects.filter(showtime=showtime, seat_number=seat_number).exists()}, status=200)

@api_view(['GET'])
def get_promotion(request, name):
    promotion = Promotion.objects.get(name=name)
    return JsonResponse({"promotion": PromotionSerializer(promotion).data}, status=200)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_movie(request):
    movie = Movie.objects.create(
        title = request.data.get("title"),
        description = request.data.get("description"),
        trailer_link = request.data.get("trailer_link"),
        img_link = request.data.get("img_link"),
        duration = request.data.get("duration"),
        release_date = datetime.strptime(request.data.get("release_date"), "%Y-%m-%d")
    )
    return JsonResponse({"movie": MovieSerializer(movie).data}, status=201)


@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_movie(request, id):
    movie = Movie.objects.get(id=id)
    movie.title = request.data.get("title")
    movie.description = request.data.get("description")
    movie.trailer_link = request.data.get("trailer_link")
    movie.img_link = request.data.get("img_link")
    movie.duration = request.data.get("duration")
    movie.release_date = datetime.strptime(request.data.get("release_date"), "%Y-%m-%d")
    movie.save()
    return JsonResponse({"movie": MovieSerializer(movie).data}, status=200)

@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_movie(request, id):
    movie = Movie.objects.get(id=id)
    movie.delete()
    return JsonResponse({"message": "Movie deleted successfully"}, status=200)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_showroom(request):
    showroom = Showroom.objects.create(
        name = request.data.get("name"),
        seat_count = request.data.get("seat_count")
    )
    return JsonResponse({"showroom": ShowroomSerializer(showroom).data}, status=201)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_showroom(request, id):
    showroom = Showroom.objects.get(id=id)
    return JsonResponse({"showroom": ShowroomSerializer(showroom).data}, status=200)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_promotion(request):
    promotion = Promotion.objects.create(
        name = request.data.get("name"),
        discount_percentage = request.data.get("discount"),
    )
    return JsonResponse({"promotion": PromotionSerializer(promotion).data}, status=201)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_promotions(request):
    promotion = Promotion.objects.all()
    return JsonResponse({"promotions": PromotionSerializer(promotion, many=True).data}, status=200)



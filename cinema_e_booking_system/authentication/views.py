import datetime
from django.shortcuts import redirect, render, get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import AdminSerializer, UserSerializer, CustomerSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from v1.models import Booking, Customer, Ticket
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate



@api_view(['GET', 'PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    if request.method == 'GET':
        try:
            profile_data = {
                "first_name": request.user.customer.first_name,
                "last_name": request.user.customer.last_name,
                "email": request.user.customer.email,
                "address": request.user.customer.address,
                "phone_number": request.user.customer.phone_number,
                "subscribed_to_promotions": request.user.customer.subscribed_to_promotions,
            }
            return Response(profile_data)
        except AttributeError:
            return Response({"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        data = request.data
        current_password = data.get('current_password')
        new_password = data.get('new_password')

        # Verify current password
        user = authenticate(username=request.user.username, password=current_password)
        if not user:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        request.user.customer.first_name = data.get('first_name', request.user.customer.first_name)
        request.user.customer.last_name = data.get('last_name', request.user.customer.last_name)
        request.user.customer.address = data.get('address', request.user.customer.address)
        request.user.customer.subscribed_to_promotions = data.get('subscribed_to_promotions', request.user.customer.subscribed_to_promotions)
        # Update password if new password is provided
        if new_password:
            request.user.set_password(new_password)

        request.user.customer.save()
        request.user.save()
        return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "Not found."}, status=status.HTTP_400_BAD_REQUEST)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    print(token)
    return Response({"token": token.key, "user": serializer.data})

@api_view(['POST'])
def reset(request):
    email = request.data['email']
    try:
        print(email)
        customer = Customer.objects.get(email=email)
        user = customer.user
        token = get_random_string(12)
        user.password = make_password(token)
        user.save()
        send_mail(
            subject='Password Reset',
            message=f'Your new password is: {token}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return Response({"detail": "Password reset successful! Check your email for the new password."}, status=status.HTTP_200_OK)
    except Customer.DoesNotExist:
        return Response({"detail": "Email not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def register(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        # Save the customer instance
        serializer.save()

        # Access the associated user and generate a verification token
        user = serializer.instance.user  # Access associated User
        token = get_random_string(32)
        
        # Assign the token to the customer and save it
        customer = serializer.instance
        customer.verification_token = token
        customer.save()

        # Send the verification email with the token
        send_verification_email(user_email=request.data['email'], verification_token=token)

        return Response({"detail": "Registration successful! Please check your email to verify your account."}, status=status.HTTP_201_CREATED)
    
    # Custom error handling for registration issues (e.g., username already taken)
    errors = serializer.errors
    if "username" in errors:
        return Response({"detail": "This username is already taken. Please choose another."}, status=status.HTTP_400_BAD_REQUEST)

    return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        
def send_verification_email(user_email, verification_token):
    # Build the verification URL
    verification_url = f"http://127.0.0.1:8000/verify-email/{verification_token}/"

    # Styled email content
    email_subject = "Verify Your Email Address"
    email_body = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                color: #333;
                margin: 0;
                padding: 20px;
            }}
            .email-container {{
                max-width: 600px;
                margin: 0 auto;
                background: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 20px;
            }}
            h1 {{
                text-align: center;
                color: #4CAF50;
            }}
            p {{
                font-size: 16px;
                margin: 10px 0;
            }}
            .button {{
                display: inline-block;
                padding: 10px 20px;
                margin: 20px 0;
                font-size: 16px;
                color: white;
                background-color: #4CAF50;
                text-decoration: none;
                border-radius: 5px;
                text-align: center;
            }}
            .button:hover {{
                background-color: #45a049;
            }}
            .footer {{
                text-align: center;
                font-size: 12px;
                color: #777;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <h1>Verify Your Email</h1>
            <p>Hello,</p>
            <p>Thank you for signing up! Please click the button below to verify your email address:</p>
            <p style="text-align: center;">
                <a href="{verification_url}" class="button">Verify Email</a>
            </p>
            <p>If the button doesn’t work, copy and paste the following link into your browser:</p>
            <p><a href="{verification_url}">{verification_url}</a></p>
            <div class="footer">
                <p>&copy; {datetime.datetime.now().year} Your Company. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """

    # Send the email
    send_mail(
        subject=email_subject,
        message="This is a plain-text fallback for non-HTML email clients.",
        from_email="no-reply@yourdomain.com",
        recipient_list=[user_email],
        html_message=email_body,  # Set the HTML content
    )



@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed for {}".format(request.user.username))

@api_view(['GET'])
def verify_email(request, token):
    try:
        # Find the customer by the verification token
        customer = Customer.objects.get(verification_token=token)
        
        # Activate the user's account
        customer.account_state = 'active'
        customer.verification_token = ''  # Clear the token once verified
        customer.save()

        # Redirect to the React page with a success status
        return redirect(f"http://localhost:3000/verify-email/{token}?status=success")
    except Customer.DoesNotExist:
        # Redirect to the React page with a failure status
        return redirect(f"http://localhost:3000/verify-email/{token}?status=error")
     
@api_view(['POST'])
# Function to check if the email is existing inside the database
def check_email(request):
    email = request.data.get('email')
    
    try:
        user = Customer.objects.get(email=email)  # Check if email exists in the database
        return Response({"uid": user.pk}, status=status.HTTP_200_OK)
    except Customer.DoesNotExist:
        return Response({"detail": "Email not found"}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['POST'])
def reset_password(request):
    uid = request.data.get('uid')
    new_password = request.data.get('new_password')
    confirm_password = request.data.get('confirm_password')

    # Ensure passwords match
    if new_password != confirm_password:
        return Response({"detail": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Find the customer using the provided uid
        customer = Customer.objects.get(pk=uid)
        user = customer.user  # Access the associated User instance

        # Update the password for the user
        user.password = make_password(new_password)  # Hash the new password
        user.save()  # Save the updated user
        customer.save()

        return Response({"detail": "Password updated successfully!"}, status=status.HTTP_200_OK)
    except Customer.DoesNotExist:
        return Response({"detail": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def create_admin(request):
    serializer = AdminSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = serializer.instance.user
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def check_active_account(request):
    try:
        if request.user.customer.account_state == 'active':
            return Response({"detail": "Account is active"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Account is not active"}, status=status.HTTP_403_FORBIDDEN)
    except AttributeError:
        return Response({"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
    


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def send_order_email(request):
    data = request.data
    email = request.user.customer.email
    booking_id = data.get('booking_id')
    try:
        booking = Booking.objects.get(id=booking_id)
        tickets = Ticket.objects.filter(booking=booking)
        promotion = booking.promotion
        showtime = None
        arr = []
        total =0
        for ticket in tickets:
            arr.append(ticket.seat_number)
            showtime = ticket.showtime
            total += ticket.ticket_type.price
        print(arr)
        send_mail(
            subject='Order Confirmation',
            message=(f'Your booking for {showtime.movie.title} has been confirmed!\n'
                     f'Showtime: {showtime.time}\n'
                     f'Showroom: {showtime.showroom.name}\n'
                     f'Seat number(s): {",".join(arr)}\n'
                     f'Total price: ${round(total * (1 - promotion.discount_percentage / 100), 2)}'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return Response({"detail": "Order confirmation sent"}, status=status.HTTP_200_OK)
    except Customer.DoesNotExist:
        return Response({"detail": "Customer not found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Booking.DoesNotExist:
        return Response({"detail": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import AdminSerializer, UserSerializer, CustomerSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from v1.models import Customer
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.conf import settings
from django.contrib.auth.hashers import make_password

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializer.data})

@api_view(['POST'])
def register(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  
        user = serializer.instance.user  
        
        # Generate a unique token for email verification
        token = get_random_string(32)
        
        # Save the token in the Customer model for verification
        customer = serializer.instance
        customer.verification_token = token
        customer.save()
        
        # Send a verification email with the token
        verification_url = request.build_absolute_uri(reverse('verify-email', kwargs={'token': token}))
        send_mail(
            subject='Verify your email address',
            message=f'Click the link to verify your account: {verification_url}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.data['email']],
            fail_silently=False,
        )

        return Response({"detail": "Registration successful! Please check your email to verify your account."}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed for {}".format(request.user.username))

@api_view(['GET'])
# Function that is invoked when the email is verified 
def verify_email(request, token):
    try:
        # Find the customer by the verification token
        customer = Customer.objects.get(verification_token=token)
        
        # Activate the user's account
        customer.account_state = 'active'
        customer.verification_token = ''  # Clear the token once verified
        customer.save()

        return Response({"detail": "Email verified successfully!"}, status=status.HTTP_200_OK)
    except Customer.DoesNotExist:
        return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)


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

# @api_view(['POST'])
# def create_admin(request):
#     serializer = AdminSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         user = serializer.instance.user
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

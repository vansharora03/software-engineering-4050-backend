from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, CustomerSerializer
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
    token = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializer.data})

@api_view(['POST'])
def register(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  
        user = serializer.instance.user  
        # send a verification email

        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed for {}".format(request.user.username))

@api_view(['GET'])
def verify_email(request, token):
    user = ...
    if user:
        user.is_active = True
        user.save()
        return Response({"detail": "Email verified successfully!"})
    return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
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

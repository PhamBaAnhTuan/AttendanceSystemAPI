# Database
from django.contrib.auth.models import User

from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.http import HttpRequest
# serializers
from .serializers import UserSerializers

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from oauth2_provider.views import TokenView
from oauth2_provider.contrib.rest_framework.permissions import OAuth2Authentication
import json

import os
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

class UserViewSet(viewsets.ModelViewSet):
   authentication_classes = [OAuth2Authentication]
   permission_classes = [IsAuthenticated]
   
   queryset = User.objects.all()
   serializer_class = UserSerializers
   
   @action(methods=['POST'], detail=False, url_path='signup', permission_classes=[AllowAny])
   def signup(self, request):
      serializer = UserSerializers(data=request.data)
      
      if serializer.is_valid():
         serializer.save()
         print(f"Sign up successful! {request.data.get('username')}")
         
         return Response({
            'message': 'Sign up successfully!',
            'data': request.data
         },status=status.HTTP_201_CREATED)
      else:
         print(f"Sign up error: {serializer.errors}")
         return Response({
            'error': serializer.errors,
         }, status=status.HTTP_400_BAD_REQUEST)
         
         
   @action(methods=['POST'], detail=False, url_path='signin', permission_classes=[AllowAny])
   def signIn(self, request):
      username = request.data.get('username')
      password = request.data.get('password')

      
      if username and password:
         user = authenticate(request, username=username, password=password)
         
         if user is not None:
            login(request, user)
            
            token_request = HttpRequest()
            token_request.method = 'POST'
            token_request.POST = {
               'grant_type': 'password',
               'username': username,
               'password': password,
               'client_id': CLIENT_ID,
               'client_secret': CLIENT_SECRET,
            }

            print(CLIENT_ID, '\n', CLIENT_SECRET)
            token_view = TokenView.as_view()
            response = token_view(token_request)
            response_content = json.loads(response.content.decode('utf-8'))
            if response.status_code == 200:
               user_data = UserSerializers(user).data
               return Response({
                  "message": "Sign in successfully!",
                  "access_token": response_content["access_token"],
                  "user_data": user_data
               }, status=status.HTTP_200_OK)
            else:
               return Response({"error": "Error generating token"}, status=response.status_code)
         else:
               return Response({"error": "Invalid credentials!"}, status=status.HTTP_401_UNAUTHORIZED)
      else:
         return Response({"error": "Username and password required!"}, status=status.HTTP_400_BAD_REQUEST)
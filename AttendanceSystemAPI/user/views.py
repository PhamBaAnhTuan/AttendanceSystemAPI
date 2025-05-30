import json
from django.test import RequestFactory
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse
from oauthlib.oauth2.rfc6749.utils import list_to_scope
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer, UserInfoSerializer
from django.contrib.auth import get_user_model, authenticate
from oauth2_provider.signals import app_authorized
from oauth2_provider.models import get_access_token_model
from rest_framework.decorators import action
from decouple import config
import os
from urllib.parse import urlencode
from oauth2_provider.views.mixins import OAuthLibMixin
from AttendanceSystemAPI.views.base import BaseViewSet
from rest_framework.status import (
   HTTP_200_OK,
   HTTP_201_CREATED,
   HTTP_400_BAD_REQUEST,
   HTTP_403_FORBIDDEN,
   HTTP_404_NOT_FOUND,
   HTTP_406_NOT_ACCEPTABLE,
   HTTP_500_INTERNAL_SERVER_ERROR,
   HTTP_401_UNAUTHORIZED
)
from .services.user_service import UserService

from roles.models import Role
from .filter import UserFilterBackend

from rest_framework.exceptions import NotAuthenticated, PermissionDenied

User = get_user_model()
AccessToken = get_access_token_model()


class UserViewSet(BaseViewSet, OAuthLibMixin):
    queryset=User.objects.all()
    serializer_class = UserSerializer
    filter_backends=[UserFilterBackend]
    required_alternate_scopes = {
        "list": [["admin"], ["teacher"], ["student"]],
        "retrieve": [["admin"], ["teacher"], ["student"]],
        "update": [["admin"], ["teacher"], ["student"]],
        "create": [["admin"]],
        "destroy": [["admin"]],
    }

    def get_queryset(self):
        user = self.request.user

        # 1. Người dùng chưa đăng nhập
        if not user or not user.is_authenticated:
            raise NotAuthenticated("You must be signin in to access this resource!")

        # 2. Người dùng không có role
        if not hasattr(user, 'role') or user.role is None:
            raise PermissionDenied("You do not have a role assigned!")

        # 3. Người dùng là admin
        if user.role.name == "admin":
            return User.objects.all()

        # 4. Người dùng thường → chỉ được xem chính họ
        return User.objects.filter(id=user.id)

    @action(methods=['post'], detail=False, url_path="signup", permission_classes=[AllowAny])
    def signup(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        fullname = request.data.get('fullname')
        phone_number = request.data.get('phone_number')
        address = request.data.get('address')
        avatar = request.data.get('avatar')
        date_of_birth = request.data.get('date_of_birth')
        role = request.data.get('role')

        if not email or not password:
            return Response({'detail': "Email and Password are required!"}, status=HTTP_404_NOT_FOUND)
        if User.objects.filter(email=email).exists():
            return Response({'detail': "Email already exists!"}, status=HTTP_400_BAD_REQUEST)
        if User.objects.filter(phone_number=phone_number).exists():
            return Response({'detail': "Phone number already exists!"}, status=HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(
            email=email,
            password=password,
            fullname=fullname,
            phone_number=phone_number,
            address=address,
            date_of_birth=date_of_birth,
            avatar=avatar,
            role=role
        )
        return Response(UserSerializer(user).data, status=HTTP_201_CREATED)

    @action(methods=['post'], detail=False, url_path="signin", permission_classes=[AllowAny])
    def signin(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        print(f"Client id: {config('CLIENT_ID')}")
        user = authenticate(username=username, password=password)
        scope = user.role.scope if hasattr(user, 'role') and user.role else ""
        if user:
            post_data = request.data.copy()
            post_data.update(
                {
                    "grant_type": "password",
                    "client_type": "confidential",
                    "client_id": config('CLIENT_ID'),
                    "client_secret": config('CLIENT_SECRET'),
                }
            )
            if len(scope) > 0:
                post_data.update({"scope": list_to_scope(scope)})

            factory = RequestFactory()
            new_request = factory.post('/o/token/', data=urlencode(post_data), content_type='application/x-www-form-urlencoded')

            url, headers, body, status = self.create_token_response(new_request)
            if status == 200:
                access_token = json.loads(body).get('access_token')
                if access_token is not None:
                    token = AccessToken.objects.get(token=access_token)
                    app_authorized.send(sender=self, request=request, token=token)
            response = HttpResponse(content=body, status=status)

            for k , v in headers.items():
                response[k] = v
            return response
        else:
            return Response({'detail': "Invalid credentials!"}, status=HTTP_401_UNAUTHORIZED)

    
    @action(methods=['post'], detail=False, url_path="refresh-token", permission_classes=[AllowAny])
    def refresh_token(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh_token")
        if not refresh_token or refresh_token == "null":
            return Response(
                {"error": "Invalid token"},
                status=HTTP_406_NOT_ACCEPTABLE,
            )
        print(f"Client id: {config('CLIENT_ID')}")
        post_data = request.data.copy()
        post_data.update(
            {
                "grant_type": "refresh_token",
                "client_id": config('CLIENT_ID'),
                "client_secret": config('CLIENT_SECRET'),
                "refresh_token": refresh_token,
            }
        )

        factory = RequestFactory()
        new_request = factory.post('/o/token/', data=urlencode(post_data), content_type='application/x-www-form-urlencoded')

        url, headers, body, status = self.create_token_response(new_request)
        if status == 200:
            access_token = json.loads(body).get('access_token')
            if access_token is not None:
                token = AccessToken.objects.get(token=access_token)
                app_authorized.send(sender=self, request=request, token=token)
        response = HttpResponse(content=body, status=status)

        for k , v in headers.items():
            response[k] = v
        return response
    
    @action(methods=['post'], detail=False, url_path="logout", permission_classes=[IsAuthenticated])
    def logout(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh_token")
        access_token = request.data.get("access_token")

        post_data = request.data.copy()
        post_data.update(
            {
                "client_id":  config('CLIENT_ID'),
                "client_secret": config('CLIENT_SECRET'),
                "token_type_hint": "refresh_token",
                "token": refresh_token,
            }
        )

        factory = RequestFactory()
        new_request = factory.post('/o/revoke/', data=urlencode(post_data), content_type='application/x-www-form-urlencoded')

        url, headers, body, status = self.create_revocation_response(new_request)
        if status != HTTP_200_OK:
            return Response(
                {"error": "Can not revoke refresh token."},
                status=HTTP_400_BAD_REQUEST,
            )
        
        post_data.update(
            {
                "token_type_hint": "access_token",
                "token": access_token,
            }
        )
        url, headers, body, status = self.create_revocation_response(new_request)
        if status != HTTP_200_OK:
            return Response(
                content={"error": "Can not revoke access token."},
                status=HTTP_400_BAD_REQUEST,
            )
        
        return Response({"message": "Logout success!"}, status=HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path="userinfo", permission_classes=[IsAuthenticated])
    def userinfo(self, request, *args, **kwargs):
        id = request.auth.user.id
        user = User.objects.get(id=id)
        user_serializer = UserInfoSerializer(user, context={'request': request})
        return Response(user_serializer.data, status=HTTP_200_OK)
    
    @action(methods=['post'], detail=False, url_path="change-password", permission_classes=[IsAuthenticated])
    def change_password(self, request, *args, **kwargs):
        email = request.data.get("email")
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")

        try:
            UserService.change_password(email, current_password, new_password)
            return Response({"message": "Password has been changed."}, status=HTTP_200_OK)
        except ValueError as ve:
            return Response({"message": str(ve)}, status=HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": "An error occurred."}, status=HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(methods=['post'], detail=False, url_path="forgot-password", permission_classes=[AllowAny])
    def forgot_password(self, request, *args, **kwargs):
        email = request.data.get("email")

        try:
            UserService.forgot_password(email)
            return Response({"message": "The link has been sent."}, status=HTTP_200_OK)
        except Exception as e:
            return Response({"message": "An error occurred."}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(methods=['post'], detail=False, url_path="reset-password", permission_classes=[AllowAny])
    def reset_password(self, request, *args, **kwargs):
        token = request.data.get("token")
        new_password = request.data.get("new_password")

        try:
            UserService.reset_password(token, new_password)
            return Response({"message": "Password has been reset."}, status=HTTP_200_OK)
        except Exception as e:
            return Response({"message": "An error occurred."}, status=HTTP_500_INTERNAL_SERVER_ERROR)
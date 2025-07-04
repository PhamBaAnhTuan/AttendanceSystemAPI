from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .models import Role
from .serializer import RoleSerializer

class RoleViewSet(ModelViewSet):
    permission_classes=[AllowAny]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    # required_alternate_scopes = {action: [["admin"]] for action in ["list", "retrieve"]}
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Client, Driver
from .permissions import IsAdmin, IsClient, IsDriver
from .serializers import ClientSerializer, DriverSerializer


class ClientViewSet(viewsets.ModelViewSet):
    """Vista para CRUD de clientes"""
    queryset = Client.objects.select_related('user').all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,IsAdmin | IsClient]

class DriverViewSet(viewsets.ModelViewSet):
    """Vista para CRUD de conductores"""
    queryset = Driver.objects.select_related('user').all()
    serializer_class = DriverSerializer
    permission_classes  = [IsAuthenticatedOrReadOnly, IsAdmin | IsDriver]



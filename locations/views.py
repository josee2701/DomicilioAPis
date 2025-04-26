from django.shortcuts import render
# Create your views here.
from rest_framework import viewsets

from .models import Address
from .serializers import AddressSerializer


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get_queryset(self):
        # Filtrar direcciones por cliente
        client_id = self.request.query_params.get('client_id')
        if client_id:
            return self.queryset.filter(client_id=client_id)
        return self.queryset
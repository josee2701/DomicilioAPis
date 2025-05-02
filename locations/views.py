# locations/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from accounts.permissions import IsAdmin, IsClient

from .models import Address
from .serializers import AddressSerializer


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdmin | IsClient]

    def get_queryset(self):
        qs = super().get_queryset()
        client_id = self.kwargs.get('client_id')
        if not client_id:
            client_id = self.request.query_params.get('client_id')
        if client_id:
            qs = qs.filter(client_id=client_id)
        return qs

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

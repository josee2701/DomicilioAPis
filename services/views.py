from django.shortcuts import get_object_or_404, render
# services/views.py
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

# Create your views here.
from .models import Service
from .serializers import ServiceSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        client_id = self.request.query_params.get('client_id')
        if client_id:
            qs = qs.filter(client__id=client_id)
        return qs

    @action(detail=True, methods=['post'], url_path='start-transit')
    def start_transit(self, request, pk=None):
      
        service = self.get_object()
        service.status = 'in_transit'
        service.save(update_fields=['status'])
        return Response(self.get_serializer(service).data)

    @action(detail=True, methods=['post'], url_path='complete')
    def complete(self, request, pk=None):
      
        service = self.get_object()
        service.status = 'completed'
        service.date_completed = timezone.now()
        service.save(update_fields=['status', 'date_completed'])
        return Response(self.get_serializer(service).data)

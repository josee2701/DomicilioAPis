# services/serializers.py

from haversine import Unit, haversine
from rest_framework import serializers

from accounts.models import Driver

from .models import Service


class ServiceSerializer(serializers.ModelSerializer):
    # devolveremos estos campos en la respuesta
    driver = serializers.PrimaryKeyRelatedField(read_only=True)
    eta_minutes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Service
        fields = [
            'id',
            'client',
            'pickup_address',
            'driver',
            'eta_minutes',
            'status',
            'date_aplication',
        ]
        read_only_fields = ['status', 'date_aplication'] # solo lectura

    def create(self, validated_data):
        address = validated_data['pickup_address']
        lat0, lon0 = address.lat, address.lon
        print(f"Ubicación de recogida: {lat0}, {lon0}")

        available = Driver.objects.filter(
            status='available',
            lat__isnull=False,
            lon__isnull=False
        )

        best = None
        best_dist = float('inf')
        for d in available:
            dist = haversine((lat0, lon0), (d.lat, d.lon), unit=Unit.KILOMETERS)
            
            if dist < best_dist:
                best_dist, best = dist, d
        print(dist)
        if not best:
            raise serializers.ValidationError("No hay conductores disponibles en este momento")
        velocidad_kmh = 40  
        eta = int(best_dist / velocidad_kmh * 60)  # minutos
        validated_data['driver'] = best
        validated_data['status'] = 'assigned'
        validated_data['eta_minutes'] = eta
        service = Service.objects.create(**validated_data)
        best.status = 'busy'
        best.save(update_fields=['status'])

        return service

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

    def create(self, validated_data):
        return Address.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # evita cambiar el cliente, por ejemplo
        validated_data.pop('client', None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        return instance
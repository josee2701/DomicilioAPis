from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Client, Driver

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone_number',
        ]

class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Client
        fields = ['id', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        return Client.objects.create(user=user)

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()
        return instance

class DriverSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Driver
        fields = ['id', 'user', 'status', 'lat', 'lon']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        return Driver.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user
        #Se recorre el diccionario de datos del usuario y se actualizan los atributos
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()
        #Se recorre el diccionario de datos del conductor y se actualizan los atributos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

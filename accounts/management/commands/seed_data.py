import random

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from faker import Faker

from accounts.models import Client, Driver
from locations.models import Address


class Command(BaseCommand):
    help = 'Genera datos de prueba: 5 clients, 5 drivers, 20 addresses.'

    def handle(self, *args, **options):
        fake = Faker()
        User = get_user_model()
        min_lat, max_lat = -4.227, 12.442  
        min_lon, max_lon = -79.01, -66.87 
        
        client_group, _ = Group.objects.get_or_create(name='Client')
        driver_group, _ = Group.objects.get_or_create(name='Driver')

        clients = []
        for i in range(5):
            username = f'cliente{i+1}'
            email = f'{username}@example.com'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username, email=email, password='test1234'
                )
                client = Client.objects.create(user=user)
                user.groups.add(client_group)
                clients.append(client)
                self.stdout.write(self.style.SUCCESS(f'Creado Client "{username}"'))
            else:
                client = Client.objects.get(user__username=username)
                user.groups.add(client_group)
                clients.append(client)
                self.stdout.write(self.style.WARNING(f'Client "{username}" ya existe'))

        drivers = []
        for i in range(5):
            username = f'driver{i+1}'
            email = f'{username}@example.com'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username, email=email, password='test1234'
                )
                user.groups.add(driver_group)
                lat = random.uniform(min_lat, max_lat)      
                lon = random.uniform(min_lon, max_lon)      
                driver = Driver.objects.create(
                    user=user, status='available', lat=lat, lon=lon
                )
                drivers.append(driver)
                self.stdout.write(self.style.SUCCESS(f'Creado Driver "{username}"'))
            else:
                driver = Driver.objects.get(user__username=username)
                user.groups.add(driver_group)
                drivers.append(driver)
                self.stdout.write(self.style.WARNING(f'Driver "{username}" ya existe'))

        for i in range(20):
            client = random.choice(clients)
            name = f'Dir{i+1}'
            street = fake.street_address()
            apartment = fake.secondary_address() if random.choice([True, False]) else ''
            city = fake.city()
            country = 'Colombia'
            # Coordenadas dentro de Colombia
            lat = random.uniform(min_lat, max_lat)
            lon = random.uniform(min_lon, max_lon)
            Address.objects.create(
                client=client,
                name=name,
                street=street,
                apartment=apartment,
                city=city,
                country=country,
                lat=lat,
                lon=lon,
            )
            self.stdout.write(self.style.SUCCESS(
                f'Creada Address "{name}" para {client.user.username}'
            ))

        self.stdout.write(self.style.SUCCESS('¡Datos de prueba generados correctamente!'))

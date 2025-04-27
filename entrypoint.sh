#!/bin/bash

# Retraso fijo para esperar que la base de datos esté disponible
sleep 10

# Ejecuta las migraciones
echo "Applying database migrations..."
python manage.py migrate || { echo 'Migrations failed' ; exit 1; }

# Inicia el servidor de Django
echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:9000

#!/bin/bash
set -euo pipefail

# Espera activa a la BD
until python manage.py showmigrations > /dev/null 2>&1; do
  echo "Esperando a la base de datos..."
  sleep 2
done

# Migraciones
echo "Applying database migrations..."
python manage.py migrate

# Seed inicial
echo "Seeding initial data..."
python manage.py seed_data

# ¡Arranca el servidor!
echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:9000

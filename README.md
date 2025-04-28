## 🎯 API para Asignación de Servicios

Es un sistema de asignación de servicios de domicilio, en el cual se registran a nuestros conductores indicando su ubicación, y permitir que los Clientes soliciten un servicio desde su ubicación. El sistema debe asignar automáticamente el conductor disponible más cercano y proporcionar una estimación del tiempo de llegada. 

---

## 📦 Tecnologías y herramientas

- **Python 3.x**
- **Django==5.2**
- **Django REST Framework (DRF)==3.16.0**
- **psycopg2-binary - PostgreSQL** como base de datos principal
- **haversine**
- **Faker**
- **Docker & Docker Compose** para contenedorización y despliegue
- **pgAdmin** para administración de la base de datos

---

## 📝 Requisitos

- Para que el proyecto funcione correctamente, necesitas:
- Python 3.x instalado (recomendado >=3.8).
- Docker y Docker Compose instalados.
- Clonar el repositorio y situarte en su carpeta raíz.
- Instalar las dependencias de Python:
- pip install -r requirements.txt

---

## 📁 Estructura del proyecto

```
DomicilioAPIs/                    
├── accounts/                     
│   ├── __pycache__/
│   ├── migrations/
│   │   └── __init__.py
|   ├── management/
|   |  ├── commands/                     
│   |  |  ├── __pycache__/
│   |  |  ├── __init__.py
│   |  |  └── seed_data.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   └── views.py
│
├── locations/                   
│   ├── __pycache__/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   └── views.py
│
├── services/                     
│   ├── __pycache__/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   └── views.py
│
├── config/                     
│   ├── __pycache__/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── entrypoint.sh
├── manage.py
├── README.md
└── requirements.txt

```

---

## 🚀 Instalación y arranque

1. **Clonar el repositorio**:

   ```bash
   git clone https://github.com/tu-usuario/DomicilioAPIs.git
   cd DomicilioAPIs
   ```

2. **Levantar los contenedores con Docker Compose**:

   ```bash
   docker-compose up --build
   ```

   - El servicio web quedará expuesto en el puerto **9000**
   - PostgreSQL en el puerto **5432**
   - pgAdmin en el puerto **5050**

---

## 🔧 API Endpoints principales

> Todas las rutas están bajo el prefijo `/api/` a menos que se indique lo contrario.

### Autenticación y Usuarios

- **Registro de cliente**\
  `POST /api/clients/`\
  Crea un nuevo `Client` junto a un `User` anidado.

- **Registro de conductor**\
  `POST /api/drivers/`\
  Crea un nuevo `Driver` junto a un `User` anidado y sus coordenadas `lat`/`lon`.

- **Actualizar usuario**\
  `PUT /api/clients/{id}/`\
  `PUT /api/drivers/{id}/`

### Direcciones (Locations)

- **Crear dirección**\
  `POST /api/addresses/`\
  Campos: `street`, `city`, `lat`, `lon`, `client` (ID)

- **Listar / editar / eliminar**\
  `GET/PUT/DELETE /api/addresses/{id}/`

### Servicios (Services)

- **Solicitar servicio**\
  `POST /api/services/`\
  Cuerpo mínimo:

  ```json
  {
    "client": 1,
    "pickup_address": 5
  }
  ```

  - El sistema calcula la distancia entre la dirección de recogida y cada conductor disponible.
  - Asigna el conductor **más cercano** y actualiza su `status` a `busy`.
  - Devuelve `driver` asignado y `eta_minutes` estimado.

- **Listar servicios**\
  `GET /api/services/services/`

- **Obtener / actualizar estado**\
  `GET/PUT /api/services/services/{id}/`

---

## ⚙️ Lógica de asignación de conductor

En `services/serializers.py`, el método `create()` de `ServiceSerializer` implementa la lógica de asignación:

1. Obtiene latitud/longitud de la dirección (`pickup_address`).
2. Filtra `Driver.objects.filter(status='available', lat__isnull=False, lon__isnull=False)`.
3. Calcula la distancia usando la función `haversine` (KM).
4. Selecciona el conductor con **menor distancia**.
5. Calcula un ETA aproximado (`best_dist / 40 km/h * 60 min`).
6. Crea la instancia `Service` con `status='assigned'` y `eta_minutes`.
7. Cambia el `status` del conductor a `busy`.

---

## 🐳 Docker Compose

El archivo `docker-compose.yml` define:

```yaml
services:
  backend:
    build: .
    command: ./entrypoint.sh
    ports:
      - "9000:9000"
    volumes:
      - ./:/domicilio
    depends_on: [db]

  db:
    image: postgres:latest
    environment:
      POSTGRES_DB: mydatabase
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
    ports: ["5432:5432"]
    volumes:
      - postgres_data:/var/lib/postgresql/data

  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@admin.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports: ["5050:80"]
    depends_on: [db]

volumes:
  postgres_data:
```

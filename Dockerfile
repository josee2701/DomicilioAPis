FROM python:3.12.4-slim

WORKDIR /domicilio

# Instala dependencias Python
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copia la app y el entrypoint
COPY . /domicilio
COPY entrypoint.sh /domicilio/entrypoint.sh
RUN chmod +x /domicilio/entrypoint.sh

EXPOSE 9000
ENTRYPOINT ["/domicilio/entrypoint.sh"]


FROM python:3.11-slim

# Instala git y otras dependencias del sistema
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean

# Clona el repositorio (ajusta con tu URL real)
RUN git clone https://github.com/YoshuaPariona/cs-final-to-do.git

# Establece el directorio de trabajo
WORKDIR /app

# Instala dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Expón el puerto (ajústalo según tu app)
EXPOSE 8000

# Comando por defecto (ajusta a lo que necesites)
CMD ["python", "main.py"]


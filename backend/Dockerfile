# Usamos una imagen base de Python 3.11
FROM python:3.11

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos los archivos de dependencias primero para aprovechar la caché de Docker
COPY requirements.txt .

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código fuente al contenedor
COPY . .

# Definimos las variables de entorno
ENV PYTHONUNBUFFERED=1
ENV MONGO_URI=mongodb://mongo:27017/serenistay

# Exponemos el puerto en el que corre FastAPI
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8000"]

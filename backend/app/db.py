from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener la URI desde el .env
uri = os.getenv("MONGO_URI")

if not uri:
    raise ValueError("⚠️ MONGO_URI no está configurado en el .env")

# Conectar con MongoDB
client = AsyncIOMotorClient(uri)
db = client["serenistay"]

# Colecciones
users_collection = db["users"]
spas_collection = db["spas"]
services_collection = db["services"]
bookings_collection = db["bookings"]
reviews_collection = db["reviews"]

# Función para probar la conexión
async def check_connection():
    try:
        await client.admin.command("ping")
        print("✅ Conexión exitosa a MongoDB desde Python")
    except Exception as e:
        print("❌ Error al conectar a MongoDB:", e)

# Prueba la conexión
if __name__ == "__main__":
    asyncio.run(check_connection())

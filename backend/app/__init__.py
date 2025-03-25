from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as list_users_router
from app.api.v1.spas import router as spas
from app.api.v1.reservations import router as reservations
from app.api.v1.services import router as services
from app.api.v1.reviews import router as reviews

# Crear una instancia de la aplicación FastAPI
app = FastAPI()


# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto por los dominios permitidos en producción
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los headers
)

app.include_router(auth_router)
app.include_router(list_users_router)
app.include_router(spas)
app.include_router(services)
app.include_router(reviews)
app.include_router(reservations)

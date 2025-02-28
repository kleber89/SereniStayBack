from fastapi import FastAPI
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as list_users_router
from app.api.v1.spas import router as spas

app = FastAPI()

@app.get("/")
async def hola():
    return {"mensaje": "si funciona"}


app.include_router(auth_router)
app.include_router(list_users_router)
app.include_router(spas)

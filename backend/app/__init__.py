from fastapi import FastAPI

# Crear una instancia de la aplicación FastAPI
app = FastAPI()

# Ruta de prueba para verificar que el servidor funciona correctamente
@app.get("/")
def read_root():
    return {"message": "¡Hola, FastAPI está funcionando!"}
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.services import facade
from datetime import timedeltal
from fastapi_jwt_auth import AuthJWT
import jwt

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Modelo para la petición de inicio de sesión
class LoginRequest(BaseModel):
    email: str
    password: str

# Modelo para la respuesta con el token
class LoginResponse(BaseModel):
    access_token: str

# Configuración del JWT(sello para el token)
class Settings(BaseModel):
    authjwt_secret_key: str = "supersecret"

@AuthJWT.load_config
def get_config():
    return Settings()

@router.post("/login", response_model=LoginResponse)
def login(credentials: LoginRequest, Authorize: AuthJWT = Depends()):
    """
    Autentica al usuario y devuelve un token JWT.
    """
    user = facade.get_user_by_email(como se van a llamr en la bse de datos.email)
    
    if not user or not user.verify_password(credentials.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = Authorize.create_access_token(
        subject={"id": user.id, "is_admin": user.is_admin},
        expires_time=timedelta(hours=1)
    )

    return {"access_token": access_token}

@router.get("/protected")
def protected(Authorize: AuthJWT = Depends()):
    """
    Un endpoint protegido que requiere un token JWT válido.
    """
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return {"message": f"Hello, user {current_user['id']}"}

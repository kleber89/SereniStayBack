from passlib.context import CryptContext
from fastapi import HTTPException, Depends, status
from datetime import datetime, timedelta
import os
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from app.models.user import User
from app.services.facade import Facade

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Checks if the plain text password matches the hash.
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta):
    """
    Create a JWT token with expiration.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    
    # Debug: Asegurarnos de que role y sub están en el token
    print("Creating token with data:", to_encode)

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

async def get_current_user(token: str = Depends(oauth2_scheme), facade: Facade = Depends()):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")

        print("Decoded JWT payload:", payload)

        if not email or not role:
            print("Error: Missing email or role in token")
            raise credentials_exception

        user_data = await facade.get_user_by_attribute("email", email)

        if not user_data:
            print(f"Error: User with email {email} not found")
            raise credentials_exception

        # 🔹 Convertir user_data en una instancia de User
        user = User(**user_data)  
        return user

    except JWTError:
        print("Error: Invalid token")
        raise credentials_exception

async def require_owner(user: User = Depends(get_current_user)):
    print("User received in require_owner:", user, type(user))  # 🔹 Debug

    if not user.role:
        print("Error: User role is missing")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User role is not defined"
        )

    if user.role.lower() != "owner":
        print(f"Error: Unauthorized role {user.role}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permissions to perform this action"
        )

    return user

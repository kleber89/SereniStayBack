from fastapi import APIRouter, HTTPException, Depends
from app.services.facade import Facade
from app.models.user import Create_User
from app.api.v1.auth_utils import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta


router = APIRouter()
facade = Facade()

@router.post("/register", summary="User register", tags=["Authentication"])
async def register(user: Create_User):
    try:
        
        user_data = user.model_dump()
        result = await facade.create_user(user_data)
        return {"message": "Successfully registered user", "id": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", summary="User login", tags=["Authentication"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await facade.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": user.email, "role": user.role}, timedelta(minutes=60))
    return {"access_token": access_token, "token_type": "bearer"}

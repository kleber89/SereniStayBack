from fastapi import APIRouter, HTTPException, Depends
from app.services.facade import Facade
from app.api.v1.auth_utils import require_owner
from app.models.spa import Spa, CreateSpa, SpaWithServices
from typing import List


router = APIRouter()
facade = Facade()


@router.post("/api/v1/create_spa", response_model=Spa)
async def create_spa(spa: CreateSpa, current_user=Depends(require_owner)):  # solo Owners pueden crear
    if current_user.role != "Owner":  # Verificamos el rol
        raise HTTPException(status_code=403, detail="Only Owners can create spas")
    
    spa.owner_id = str(current_user.id)  # Asignamos el owner_id
    return await facade.create_spa(spa.model_dump())


@router.get("/api/v1/spas", response_model=List[SpaWithServices])  # Importante: usar el nuevo modelo
async def get_spas():
    return await facade.list_spas()

from fastapi import APIRouter, HTTPException, Depends
from app.services.facade import Facade
from app.api.v1.auth_utils import require_owner
from app.models.spa import Spa, CreateSpa
from typing import List, Dict, Any

router = APIRouter()
facade = Facade()

#@router.post("/create_spa", response_model=Spa)   AQUI YA SE PUEDE CREAR EL SPA, PERO FALTA VERIFICAR EL ROL
#async def create_spa(spa: CreateSpa):
#    await facade.spa_db.add(spa.model_dump())
#    return spa

@router.post("/create_spa", response_model=Spa)
async def create_spa(spa: CreateSpa, current_user=Depends(require_owner)):  # solo Owners pueden crear
    if current_user.role != "Owner":  # Verificamos el rol
        raise HTTPException(status_code=403, detail="Only Owners can create spas")
    
    spa.owner_id = str(current_user.id)  # Asignamos el owner_id
    return await facade.create_spa(spa.model_dump())


@router.get("/spas", response_model=List[Spa])
async def list_spas():
    """List all available spas"""
    return await facade.get_all_spas()

@router.get("/spas/{spa_id}", response_model=Spa)
async def get_spa(spa_id: str):
    """Get details of a single spa"""
    spa = await facade.get_spa_by_id(spa_id)
    if not spa:
        raise HTTPException(status_code=404, detail="Spa not found")
    return spa

@router.post("/spas/{spa_id}/services", response_model=Dict[str, Any])
async def add_service_to_spa(spa_id: str, service_data: Dict[str, Any], current_user=Depends(require_owner)):
    """Add a service to a spa (Only Owners)"""
    spa = await facade.get_spa_by_id(spa_id)
    if not spa:
        raise HTTPException(status_code=404, detail="Spa not found")
    
    if spa.owner_id != str(current_user.id):
        raise HTTPException(status_code=403, detail="You do not own this spa")

    new_service = await facade.add_service_to_spa(spa_id, service_data)
    return new_service

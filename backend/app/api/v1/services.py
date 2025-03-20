from fastapi import APIRouter, Depends, HTTPException
from app.services.facade import Facade
from app.models.service import CreateService
from app.api.v1.auth_utils import require_owner
from typing import List


router = APIRouter()
facade = Facade()


@router.post("/api/v1/create_service")
async def create_service(services: List[CreateService], current_user=Depends(require_owner)):
    if current_user.role != "Owner":
        raise HTTPException(status_code=403, detail="Only Owners can create services")

    return await facade.create_multiple_services([s.model_dump() for s in services])


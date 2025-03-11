from fastapi import APIRouter, HTTPException, Depends
from app.services.facade import Facade
from app.api.v1.auth_utils import require_owner
from app.models.user import User
from typing import List

router = APIRouter()
facade = Facade()

@router.get("/api/v1/users", response_model=List[User])
async def list_all_users(current_user: User = Depends(require_owner), facade: Facade = Depends()):
    """List all users"""

    return await facade.get_all_users()


@router.get("/users/{id_user}", dependencies=[Depends(require_owner)])
async def list_user(id_user: str, current_user: User = Depends(require_owner), facade: Facade = Depends()):
    """List one user by id"""

    user = await facade.get_user_by_id(id_user)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

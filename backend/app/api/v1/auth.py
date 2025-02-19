from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/register")
#new_user = await facade.create_user(user.model_dump())

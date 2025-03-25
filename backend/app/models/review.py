from app.models.base_model import BaseEntity
from pydantic import Field

class Review(BaseEntity):
    spa_id: str
    user_id: str
    commentary: str = Field(..., min_length=1, max_length=100)
    rating: int = Field(..., ge=1, le=5)

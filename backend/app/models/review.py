from app.models.base_model import BaseEntity
from pydantic import Field, field_validator
from typing import Annotated

class Review(BaseEntity):
    spa_id: Annotated[str, Field(...)]
    user_id: Annotated[str, Field(...)]
    commentary: str = Field(..., min_length=1, max_length=50)
    rating: int = Field(..., ge=1, le=5)

    @field_validator("rating", mode="before")
    @classmethod
    def verify_rating(cls, value):
        if value < 1 or value > 5:
            raise ValueError("Rating must be between 1 and 5")
        return value


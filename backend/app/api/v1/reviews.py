from fastapi import APIRouter, HTTPException
from app.services.facade import Facade


router = APIRouter()
facade = Facade()

    

@router.post("/api/v1/spas/{spa_id}/reviews", summary="Create a review for a spa", tags=["Reviews"])
async def create_review(spa_id: str, review_data: dict):
    """
    Creates a new review for a specific spa.
    """
    try:
        review_data["spa_id"] = spa_id  # Asegurar que la reseña tenga el ID del spa
        review = await facade.create_review(review_data)
        return review
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/api/v1/spas/{spa_id}/reviews", summary="Get all reviews for a spa", tags=["Reviews"])
async def get_reviews(spa_id: str):
    """
    Get all reviews for a specific spa.
    """
    try:
        reviews = await facade.get_reviews(spa_id)
        if not reviews:
            raise HTTPException(status_code=404, detail="No reviews found for this spa")
        return reviews
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

from fastapi import APIRouter
from backend.app.services.crewai_service import get_recommendation
from backend.app.schemas.ai import RecommendationResponse

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/recommendation", response_model=RecommendationResponse)
async def generate_recommendation(user_id: int):
    result = await get_recommendation(user_id)
    return result

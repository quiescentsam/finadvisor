from pydantic import BaseModel
from typing import List

class RecommendationResponse(BaseModel):
    user_id: int
    advice: List[str]

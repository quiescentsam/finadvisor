async def get_recommendation(user_id: int):
    # TODO: integrate CrewAI multi-agent logic
    return {
        "user_id": user_id,
        "advice": ["Invest in AAPL", "Consider bonds for risk management"]
    }

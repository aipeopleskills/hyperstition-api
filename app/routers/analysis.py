from fastapi import APIRouter

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"]
)

@router.get("/")
async def get_analysis_status():
    return {"message": "Endpoint de análisis en desarrollo"}

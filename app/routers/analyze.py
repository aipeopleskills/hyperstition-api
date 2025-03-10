from fastapi import APIRouter, HTTPException
from app.services.analysis import HyperstitionAnalyzer

router = APIRouter(prefix="/analysis", tags=["Analysis"])

@router.post("/")
async def analyze_text(payload: dict):
    text = payload.get("text")
    if not text:
        raise HTTPException(status_code=400, detail="Se requiere un texto para analizar")

    analyzer = HyperstitionAnalyzer(text)
    results = analyzer.full_analysis()
    
    return results

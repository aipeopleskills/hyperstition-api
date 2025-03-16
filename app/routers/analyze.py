from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.analysis import HyperstitionAnalyzer

router = APIRouter(prefix="/analysis", tags=["Analysis"])

# Modelo de entrada para validación
class TextRequest(BaseModel):
    text: str

@router.post("/")
async def analyze_text(request: TextRequest):
    """
    Endpoint para análisis de texto hipersticioso
    """
    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Se requiere un texto válido para analizar"
        )
    
    try:
        analyzer = HyperstitionAnalyzer(request.text)
        results = analyzer.full_analysis()
        return {
            "success": True,
            "data": results,
            "error": None
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en el análisis: {str(e)}"
        )
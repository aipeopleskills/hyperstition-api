from fastapi import APIRouter

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"]
)

@router.get("/", summary="Estado del servicio de análisis")
async def get_analysis_status():
    """
    Devuelve el estado actual del servicio de análisis hipersticioso
    
    Returns:
        dict: Mensaje de estado y versión del servicio
    """
    return {
        "message": "Endpoint de análisis en desarrollo",
        "status": "active",
        "version": "0.1.0-alpha",
        "endpoints_available": [
            "/analysis/ (GET) - Estado del servicio",
            "/analysis/ (POST) - Ejecutar análisis"
        ]
    }
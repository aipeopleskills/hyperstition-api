from fastapi import APIRouter

router = APIRouter(prefix="/hyperstition", tags=["Hyperstition"])

@router.get("/", summary="Endpoint principal de Hiperstición")
async def get_hyperstition():
    return {"message": "Bienvenido al módulo de análisis hipersticioso"}

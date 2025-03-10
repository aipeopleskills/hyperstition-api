from fastapi import APIRouter, HTTPException
from app.services.database import check_db_connection
from app.services.cache import redis_cache
from app.config.settings import settings
from app.utils.logger import app_logger

# Configuración del router
router = APIRouter(
    prefix="/system",
    tags=["System"]
)

@router.get("/", summary="Mensaje de bienvenida")
async def root():
    """
    Devuelve un mensaje de bienvenida con la versión de la API.
    """
    return {"message": "Bienvenido a Hyperstition API", "version": settings.APP_VERSION}

@router.get("/health", summary="Verifica el estado del servicio")
async def health_check():
    """
    Verifica el estado operativo de la API y sus dependencias (DB y Redis).
    """
    try:
        db_status = await check_db_connection()
        redis_status = redis_cache.client.ping() if settings.USE_REDIS else "disabled"

        return {
            "status": "operational",
            "version": settings.APP_VERSION,
            "dependencies": {
                "database": db_status,
                "redis": redis_status,
                "storage": "ok" if settings.STORAGE_ENABLED else "disabled"
            }
        }
    except Exception as e:
        app_logger.error(f"Error en health check: {str(e)}")
        raise HTTPException(status_code=503, detail="Service Unavailable")

# 🔹 NUEVO: Endpoint raíz `/` sin prefijo para evitar errores 404
@router.get("/", summary="Ruta principal")
async def api_root():
    """
    Responde con un mensaje de bienvenida en la ruta raíz `/` sin prefijo.
    """
    return {"message": "Bienvenido a Hyperstition API", "version": settings.APP_VERSION}



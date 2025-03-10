from fastapi import FastAPI, APIRouter, Request, HTTPException
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

# Importaciones de configuración y servicios
from app.config.settings import settings
from app.services.database import check_db_connection, init_db, close_db_connections
from app.services.cache import redis_cache
from app.utils.logger import app_logger, security_logger, validation_logger

# Importación de routers
from app.routers import system, analysis, hyperstition

# Crear un APIRouter global sin prefijo
global_router = APIRouter()

@global_router.get("/", include_in_schema=False)
async def root():
    """Endpoint raíz de la API"""
    return {"message": "Bienvenido a Hyperstition API", "version": settings.APP_VERSION}

@global_router.get("/health", tags=["Monitoring"], summary="Estado del servicio")
async def health_check():
    """Verifica el estado operativo del servicio y sus dependencias"""
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

# Inicialización de FastAPI
app = FastAPI(
    title="Hyperstition API",
    version=settings.APP_VERSION,
    docs_url="/docs" if settings.DOCS_ENABLED else None,
    redoc_url=None,
    root_path=settings.ROOT_PATH
)

# Registrar routers en orden (APIRouter global primero)
app.include_router(global_router)
app.include_router(system.router)
app.include_router(analysis.router)
app.include_router(hyperstition.router)

# Middlewares esenciales
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    max_age=600
)

# Middleware de seguridad personalizado
@app.middleware("http")
async def security_middleware(request: Request, call_next):
    try:
        user_agent = request.headers.get("User-Agent", "unknown").lower()
        if not any(agent.lower() in user_agent for agent in settings.ALLOWED_USER_AGENTS):
            security_logger.warning(f"Intento de acceso bloqueado - User-Agent: {user_agent}")
            raise HTTPException(status_code=403, detail="Acceso no autorizado")

        response = await call_next(request)

        # Headers de seguridad
        response.headers.update({
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains"
        })

        return response

    except HTTPException as he:
        raise he
    except Exception as e:
        app_logger.critical(f"Error crítico en middleware: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Error interno del servidor"}
        )

# Manejadores globales de excepciones
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    validation_logger.error(f"Error de validación: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": "Parámetros inválidos", "errors": exc.errors()},
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Eventos de ciclo de vida
@app.on_event("startup")
async def startup_event():
    app_logger.info("🔄 Iniciando aplicación...")

    # Inicializar base de datos
    await init_db()

    # Inicializar Redis si está habilitado
    if settings.USE_REDIS:
        await redis_cache.initialize()

    app_logger.info("✅ Aplicación lista para recibir peticiones")

@app.on_event("shutdown")
async def shutdown_event():
    app_logger.info("🛑 Apagando aplicación...")

    await close_db_connections()

    if settings.USE_REDIS:
        await redis_cache.close()

    app_logger.info("🔌 Apagado completo")

# Ejecución del servidor (solo para desarrollo)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app="app.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG_MODE,
        log_config=settings.LOGGING_CONFIG,
        proxy_headers=True,
        timeout_keep_alive=30
    )

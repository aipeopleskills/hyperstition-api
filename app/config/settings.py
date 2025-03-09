from pydantic_settings import BaseSettings  # ✅ Corregida la importación

class Settings(BaseSettings):
    """Configuraciones de la aplicación."""

    # Información básica de la API
    APP_VERSION: str = "1.0.0"
    DOCS_ENABLED: bool = True
    ROOT_PATH: str = ""

    # Configuración del servidor
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    DEBUG_MODE: bool = True
    LOGGING_CONFIG: str = "logging.conf"

    # Seguridad y CORS
    ALLOWED_HOSTS: list[str] = ["*"]  # Permite todas las conexiones (ajústalo si es necesario)
    CORS_ALLOWED_ORIGINS: list[str] = ["*"]  # Permitir todas las solicitudes CORS

    # User-Agents permitidos para acceder a la API
    ALLOWED_USER_AGENTS: list[str] = ["Mozilla", "Chrome", "Firefox", "Postman", "curl"]

    # Configuración de Neo4j
    USE_NEO4J: bool = True
    NEO4J_URI: str = "bolt://neo4j:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "hyperstition"

    # Configuración de Redis
    USE_REDIS: bool = True
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    # Configuración de almacenamiento (habilitar si se usa almacenamiento externo)
    STORAGE_ENABLED: bool = True

# Instancia global de configuración
settings = Settings()

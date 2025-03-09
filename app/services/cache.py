import redis
import asyncio

REDIS_URL = "redis://redis:6379"

class RedisCache:
    def __init__(self, url: str):
        self.url = url
        self.client = None

    async def initialize(self):
        """Inicializa la conexión a Redis."""
        loop = asyncio.get_event_loop()
        self.client = redis.Redis.from_url(
            self.url, decode_responses=True, socket_timeout=5, socket_connect_timeout=5
        )
        try:
            # Verifica si Redis está disponible
            pong = self.client.ping()
            if pong:
                print("✅ Conexión a Redis establecida correctamente.")
            else:
                print("⚠️ No se pudo conectar a Redis.")
        except redis.ConnectionError as e:
            print(f"❌ Error de conexión a Redis: {str(e)}")
            self.client = None

    async def close(self):
        """Cierra la conexión a Redis."""
        if self.client:
            self.client.close()
            print("🔌 Conexión a Redis cerrada.")

# Instancia global del cliente Redis
redis_cache = RedisCache(REDIS_URL)

async def get_redis_pool():
    """Retorna la instancia global de Redis."""
    return redis_cache.client

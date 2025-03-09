import asyncio
from neo4j import GraphDatabase

# Configurar conexión a Neo4j
NEO4J_URI = "bolt://neo4j:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "hyperstition"

# Crear driver de conexión
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

async def check_db_connection():
    """Verifica si la conexión con Neo4j es exitosa."""
    loop = asyncio.get_event_loop()
    try:
        def query(tx):
            return tx.run("RETURN 'Conexión exitosa' AS message").single()["message"]
        
        result = await loop.run_in_executor(None, lambda: driver.session().read_transaction(query))
        return result
    except Exception as e:
        raise RuntimeError(f"Error de conexión a Neo4j: {str(e)}") from e

async def init_db():
    """Inicializa la base de datos creando índices y estructuras necesarias."""
    loop = asyncio.get_event_loop()
    try:
        def create_constraints(tx):
            tx.run("CREATE CONSTRAINT IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE")
            tx.run("CREATE CONSTRAINT IF NOT EXISTS FOR (p:Post) REQUIRE p.id IS UNIQUE")

        await loop.run_in_executor(None, lambda: driver.session().write_transaction(create_constraints))
        print("✅ Base de datos inicializada correctamente.")
    except Exception as e:
        raise RuntimeError(f"❌ Error al inicializar la base de datos: {str(e)}") from e

async def close_db_connections():
    """Cierra la conexión con la base de datos de forma segura."""
    try:
        driver.close()
        print("🔌 Conexión a Neo4j cerrada correctamente.")
    except Exception as e:
        print(f"⚠️ Error al cerrar la conexión: {str(e)}")

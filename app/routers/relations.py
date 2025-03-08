from fastapi import APIRouter, Depends, HTTPException, Body
from app.models.schemas import RelationCreate  # Asegúrate de tener este modelo
from app.utils.neo4j_connector import Neo4jConnector

router = APIRouter(prefix="/relations", tags=["Relations"])

@router.post("/")
async def create_relation(
    relation_data: RelationCreate = Body(...),  # Usar Body para recibir JSON
    connector: Neo4jConnector = Depends()
):
    try:
        with connector.driver.session() as session:
            result = session.run(
                """MATCH (a:Node {id: $source_id}), (b:Node {id: $target_id})
                   CREATE (a)-[r:RELATION {type: $rel_type}]->(b)
                   RETURN r""",
                source_id=relation_data.source_id,
                target_id=relation_data.target_id,
                rel_type=relation_data.relation_type
            )
            return result.single().data()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
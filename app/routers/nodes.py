from fastapi import APIRouter, Depends, HTTPException
from app.utils.neo4j_connector import Neo4jConnector

router = APIRouter(prefix="/nodes", tags=["Nodes"])

@router.post("/")
async def create_node(node_data: dict, connector: Neo4jConnector = Depends()):
    try:
        with connector.driver.session() as session:
            result = session.execute_write(
                lambda tx: tx.run(
                    "CREATE (n:Node $props) RETURN n",
                    props=node_data
                )
            )
            return result.single().data()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
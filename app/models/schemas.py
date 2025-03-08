from pydantic import BaseModel

class RelationCreate(BaseModel):
    source_id: str
    target_id: str
    relation_type: str
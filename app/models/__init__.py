from pydantic import BaseModel

class NodeCreate(BaseModel):
    id: str
    name: str
    type: str

class RelationCreate(BaseModel):
    source_id: str
    target_id: str
    relation_type: str
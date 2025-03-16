from pydantic import BaseModel

class RelationCreate(BaseModel):
    source_id: str
    target_id: str
    relation_type: str

from pydantic import BaseModel
from typing import Dict, List

class RelationCreate(BaseModel):
    source_id: str
    target_id: str
    relation_type: str

class TextInput(BaseModel):
    text: str

class AnalysisResult(BaseModel):
    detected_terms: Dict[str, List[str]]
    semantic_score: float
    linguistic_complexity: Dict[str, float]
    referential_analysis: Dict[str, float]  
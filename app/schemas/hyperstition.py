from pydantic import BaseModel
from typing import Dict, List

# Esquema para análisis sintáctico
class SyntacticOutput(BaseModel):
    sentence_types: Dict[str, int]
    dependencies: List[Dict[str, str]]
    complexity: Dict[str, float]
    voice: Dict[str, int]
    negation_patterns: Dict[str, List[str]]
    subject_positions: Dict[str, int]

# Esquema principal que incluye todas las capas
class FullAnalysisOutput(BaseModel):
    hyperstition: Dict  # Asumiendo que tienes un esquema HyperstitionOutput definido
    semantics: Dict[str, float]
    syntax: SyntacticOutput  # Nueva sección
    risk_profile: Dict[str, str]
    discourse_style: str

# Si usas otros esquemas, importalos:
# from .hyperstition import HyperstitionOutput
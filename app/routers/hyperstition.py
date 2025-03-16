########################################################
###  HYPERSTITION API - v2.2 (Stable Sync Build)    ###
########################################################

# ---------------
# 1. IMPORTS ESENCIALES
# ---------------
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Dict, List, Any
from pathlib import Path
from datetime import datetime
import spacy
import json
import re
import logging

# ---------------
# 2. CONFIGURACIÓN BÁSICA
# ---------------
router = APIRouter(prefix="/hyperstition", tags=["Hyperstition"])
nlp = spacy.load("es_core_news_md")
logger = logging.getLogger("hyperstition-core")
logger.setLevel(logging.INFO)

DICTIONARY_PATH = Path("app/data/hyperstition_terms.json")
API_VERSION = "2.2"

# ---------------
# 3. MODELOS PYDANTIC
# ---------------
class TextInput(BaseModel):
    """Modelo de entrada para el texto a analizar."""
    text: str

class HyperstitionOutput(BaseModel):
    """Modelo de salida con los resultados del análisis."""
    detected_terms: Dict[str, List[str]]
    semantic_score: float
    risk_level: str
    linguistic_complexity: Dict[str, float]
    referential_analysis: Dict[str, float]
    syntactic_analysis: Dict[str, Any]
    cognitive_profile: Dict[str, Any]
    metadata: Dict[str, str]

# ---------------
# 4. CARGA DINÁMICA DE RECURSOS
# ---------------
def load_hyperstition_resources() -> Dict:
    """Carga y valida el diccionario desde el JSON."""
    try:
        # Verificar que el archivo JSON exista
        if not DICTIONARY_PATH.exists():
            raise FileNotFoundError(f"Archivo JSON no encontrado: {DICTIONARY_PATH}")

        # Cargar el JSON
        with open(DICTIONARY_PATH, "r", encoding="utf-8") as f:
            full_data = json.load(f)

        # Validar estructura básica
        if "categorias" not in full_data:
            raise ValueError("El JSON debe contener la clave 'categorias'")
        if "metadatos" not in full_data or "pesos_analiticos" not in full_data["metadatos"]:
            raise ValueError("El JSON debe contener 'metadatos.pesos_analiticos'")

        # Extraer categorías y pesos
        categories = full_data["categorias"]
        weights = full_data["metadatos"]["pesos_analiticos"]

        # Validar que todas las categorías tengan un peso
        missing_weights = set(categories.keys()) - set(weights.keys())
        if missing_weights:
            raise ValueError(
                f"Las siguientes categorías no tienen un peso definido: {missing_weights}"
            )

        # Retornar recursos cargados
        return {
            "categories": categories,
            "weights": weights,
            "metadata": full_data.get("metadatos", {})
        }

    except json.JSONDecodeError as e:
        logger.error(f"Error al decodificar el JSON: {str(e)}")
        return {"categories": {}, "weights": {}, "metadata": {}}
    except Exception as e:
        logger.error(f"Error al cargar recursos: {str(e)}")
        return {"categories": {}, "weights": {}, "metadata": {}}

# ---------------
# 5. INICIALIZACIÓN GLOBAL
# ---------------
resources = load_hyperstition_resources()
HYPERSTITION_DICT = resources["categories"]
HYPERSTITION_WEIGHTS = resources["weights"]
DICT_METADATA = resources["metadata"]

logger.info(f"🔑 Pesos analíticos cargados: {HYPERSTITION_WEIGHTS}")
logger.info(f"📚 Categorías disponibles: {list(HYPERSTITION_DICT.keys())}")

# ---------------
# 6. FUNCIONES CORE
# ---------------
def detect_hyperstition_terms(text: str) -> Dict[str, List[str]]:
    """Detección de términos con soporte multi-categoría."""
    detected = {}
    for category, terms in HYPERSTITION_DICT.items():
        found_terms = [
            term for term in terms 
            if re.search(rf"\b{re.escape(term)}\b", text, re.IGNORECASE)
        ]
        if found_terms:
            detected[category] = found_terms
    return detected

def analyze_referential(text: str) -> Dict[str, float]:
    """Análisis de marcas referenciales en el texto."""
    referential = {"yo": 0.0, "nosotros": 0.0, "ellos": 0.0, "neutro": 0.0}
    words = text.lower().split()
    total = len(words) or 1
    
    referential["yo"] = round(sum(1 for w in words if w in ["yo", "mí", "me"]) / total, 2)
    referential["nosotros"] = round(sum(1 for w in words if w in ["nosotros", "nuestro"]) / total, 2)
    referential["ellos"] = round(sum(1 for w in words if w in ["ellos", "su", "les"]) / total, 2)
    referential["neutro"] = round(sum(1 for w in words if w in ["según", "expertos"]) / total, 2)
    
    return referential

def analyze_linguistic_complexity(text: str) -> Dict[str, float]:
    """Cálculo de métricas de complejidad lingüística."""
    doc = nlp(text)
    words = [token.text for token in doc if not token.is_punct]
    syllables = sum([max(1, len(re.findall(r'[aeiouáéíóú]+', word.lower()))) for word in words])
    
    return {
        "avg_sentence_length": round(len(words) / len(list(doc.sents)), 2) if doc.sents else 0,
        "avg_syllables_per_word": round(syllables / len(words), 2) if words else 0,
        "long_word_ratio": round(len([w for w in words if len(w) > 7]) / len(words), 2) if words else 0
    }

def calculate_semantic_score(detected_terms: Dict) -> float:
    """Cálculo dinámico del score semántico."""
    if not detected_terms:
        return 0.0
    
    total_score = sum(
        len(terms) * HYPERSTITION_WEIGHTS.get(category, 1.0)
        for category, terms in detected_terms.items()
    )
    return round(total_score / len(detected_terms), 3)

# ---------------
# 7. ANALIZADORES ESPECIALIZADOS
# ---------------
class SyntacticAnalyzer:
    """Analizador sintáctico completo con detección de estructuras complejas."""
    
    def analyze(self, text: str) -> Dict[str, Any]:
        doc = nlp(text)
        return {
            "sentence_types": self._detect_sentence_types(doc),
            "dependencies": self._extract_dependencies(doc),
            "complexity": self._calculate_complexity(doc)
        }

    def _detect_sentence_types(self, doc) -> Dict:
        types = {"declarative": 0, "interrogative": 0, "exclamative": 0}
        for sent in doc.sents:
            if '?' in sent.text:
                types["interrogative"] += 1
            elif '!' in sent.text:
                types["exclamative"] += 1
            else:
                types["declarative"] += 1
        return types

    def _extract_dependencies(self, doc) -> List[Dict]:
        return [{
            "governor": token.head.text,
            "dependent": token.text,
            "relation": token.dep_
        } for token in doc if token.dep_ not in ["punct", "space"]]

    def _calculate_complexity(self, doc) -> Dict:
        return {
            "subordinate_clauses": sum(1 for sent in doc.sents if "mark" in [t.dep_ for t in sent]),
            "depth_score": round(sum(len(list(token.subtree)) for token in doc) / len(doc), 2)
        }

class CognitiveIntegrator:
    """Integrador cognitivo con cálculo de vectores de riesgo."""
    
    def generate_profile(self, detected_terms: Dict) -> Dict:
        risk_vectors = {
            category: len(terms) * HYPERSTITION_WEIGHTS.get(category, 1.0)
            for category, terms in detected_terms.items()
        }
        return {
            "risk_vectors": risk_vectors,
            "total_risk": round(sum(risk_vectors.values()), 2)
        }

# ---------------
# 8. ENDPOINT PRINCIPAL
# ---------------
@router.post("/analyze", response_model=HyperstitionOutput)
async def full_analysis(input: TextInput):
    """Endpoint principal para análisis hipersticial."""
    try:
        # Validación básica
        if len(input.text) < 15:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Texto insuficiente para análisis (mínimo 15 caracteres)"
            )

        # Procesamiento paralelo
        detected_terms = detect_hyperstition_terms(input.text)
        semantic_score = calculate_semantic_score(detected_terms)
        risk_level = "Bajo" if semantic_score < 0.1 else "Moderado" if semantic_score < 0.3 else "Alto"

        return {
            "detected_terms": detected_terms,
            "semantic_score": semantic_score,
            "risk_level": risk_level,
            "linguistic_complexity": analyze_linguistic_complexity(input.text),
            "referential_analysis": analyze_referential(input.text),
            "syntactic_analysis": SyntacticAnalyzer().analyze(input.text),
            "cognitive_profile": CognitiveIntegrator().generate_profile(detected_terms),
            "metadata": {
                "version": API_VERSION,
                "dictionary_version": DICT_METADATA.get("version", "N/A"),
                "timestamp": datetime.utcnow().isoformat()
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en análisis: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del sistema v{API_VERSION}"
        )

# ---------------
# 9. VERIFICACIÓN INICIAL
# ---------------
if __name__ == "__main__":
    # Prueba de carga básica
    test_text = "El neurocapitalismo y la algocracia predictiva aceleran el colapso geopolítico."
    print("=== PRUEBA DE DETECCIÓN ===")
    print(detect_hyperstition_terms(test_text))
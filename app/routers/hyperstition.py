from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import spacy
import json
import os
import re
import gensim

# 🔹 Cargar el modelo de NLP
nlp = spacy.load("es_core_news_md")

# 🔹 Definir el router
router = APIRouter(prefix="/hyperstition", tags=["Hyperstition"])

# 🔹 Modelo de entrada
class TextInput(BaseModel):
    text: str

# 🔹 Ruta del diccionario hipersticioso
DICTIONARY_PATH = "app/data/hyperstition_terms.json"

# 🔹 Cargar el diccionario hipersticioso
if os.path.exists(DICTIONARY_PATH):
    with open(DICTIONARY_PATH, "r", encoding="utf-8") as file:
        HYPERSTITION_DICTIONARY = json.load(file).get("categorias", {})
else:
    HYPERSTITION_DICTIONARY = {}

# 🔹 Ponderación de cada categoría
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import spacy
import json
import os
import re
import gensim

# 🔹 Cargar el modelo de NLP
nlp = spacy.load("es_core_news_md")

# 🔹 Definir el router
router = APIRouter(prefix="/hyperstition", tags=["Hyperstition"])

# 🔹 Modelo de entrada
class TextInput(BaseModel):
    text: str

# 🔹 Ruta del diccionario hipersticioso
DICTIONARY_PATH = "app/data/hyperstition_terms.json"

# 🔹 Cargar el diccionario hipersticioso
if os.path.exists(DICTIONARY_PATH):
    with open(DICTIONARY_PATH, "r", encoding="utf-8") as file:
        HYPERSTITION_DICTIONARY = json.load(file).get("categorias", {})
else:
    HYPERSTITION_DICTIONARY = {}

# 🔹 Ponderación de cada categoría
HYPERSTITION_WEIGHTS = {
    "catastrofismo": 1.5,
    "utopismo": 1.2,
    "neologismos": 1.0,
    "paradojas": 1.3,
    "trampas_linguisticas": 1.1,
    "psicologismos": 1.3,
    "anglicismos": 1.0,
    "mitos_modernos": 1.5,
    "conspiraciones": 1.6,
    "futurismo_mesianico": 1.4,  # ✅ Nueva categoría
}

# 🔹 Modelo de embeddings semánticos (Word2Vec)
WORD2VEC_MODEL_PATH = "app/models/word2vec.model"

if os.path.exists(WORD2VEC_MODEL_PATH):
    word2vec_model = gensim.models.KeyedVectors.load(WORD2VEC_MODEL_PATH)
else:
    word2vec_model = None

# 🔹 Función para detectar términos en el texto con expresiones regulares
def detect_terms(text, terms):
    found_terms = []
    for term in terms:
        if re.search(rf"\b{re.escape(term.lower())}\b", text):
            found_terms.append(term)
    return found_terms

# 🔹 Función para análisis referencial (yo/nosotros/ellos/neutro)
def analyze_referential(text):
    referential_counts = {"yo": 0, "nosotros": 0, "ellos": 0, "neutro": 0}
    first_person = ["yo", "mí", "me", "mío", "mi"]
    collective = ["nosotros", "nuestro", "nos", "nuestra"]
    third_person = ["ellos", "su", "sus", "los", "las", "les"]
    neutral_terms = ["algunos", "otros", "expertos", "testigos", "gente"]

    words = text.lower().split()
    total_words = len(words)

    if total_words > 0:
        referential_counts["yo"] = sum(1 for word in words if word in first_person) / total_words
        referential_counts["nosotros"] = sum(1 for word in words if word in collective) / total_words
        referential_counts["ellos"] = sum(1 for word in words if word in third_person) / total_words
        referential_counts["neutro"] = sum(1 for word in words if word in neutral_terms) / total_words

    return referential_counts

# 🔹 Función para analizar el estilo discursivo
def detect_discourse_style(text):
    if any(word in text.lower() for word in ["urgente", "destrucción", "colapso", "crisis"]):
        return "Sensacionalista"
    elif any(word in text.lower() for word in ["gran reinicio", "nuevo orden mundial", "manipulación"]):
        return "Conspirativo"
    elif any(word in text.lower() for word in ["predicción", "estadísticas", "datos", "informe"]):
        return "Académico"
    else:
        return "Neutral"

# 🔹 Endpoint de análisis semántico
@router.post("/analyze", summary="Análisis semántico con taxonomía hipersticiosa")
async def analyze_hyperstition(input_text: TextInput):
    try:
        doc = nlp(input_text.text.lower())
        text = input_text.text.lower()

        # 🔍 Extraer términos hipersticiosos y clasificarlos
        detected_terms = {}
        total_score = 0.0

        for category, terms in HYPERSTITION_DICTIONARY.items():
            found_terms = detect_terms(text, terms)
            if found_terms:
                detected_terms[category] = {"terms": found_terms, "score": len(found_terms) * HYPERSTITION_WEIGHTS.get(category, 1.0)}
                total_score += detected_terms[category]["score"]

        # 🔍 Análisis referencial (yo/nosotros/ellos/neutro)
        referential_analysis = analyze_referential(text)

        # 🔍 Detección de estilo discursivo
        text_style = detect_discourse_style(text)

        # 🔍 Relación semántica entre términos (Word2Vec) - ✅ CORREGIDO
        semantic_relationships = {}
        if word2vec_model:
            for category, data in detected_terms.items():
                related_terms = {}
                for term in data["terms"]:
                    try:
                        similar_words = word2vec_model.wv.most_similar(term, topn=3)  # ✅ Corrección aquí
                        related_terms[term] = [word[0] for word in similar_words]
                    except KeyError:
                        related_terms[term] = []
                semantic_relationships[category] = related_terms

        # 🔍 Normalización del puntaje final
        semantic_score = round(total_score / max(1, len(doc)), 3)
        score_level = "Bajo" if semantic_score < 0.1 else "Moderado" if semantic_score < 0.3 else "Alto"

        # 🔍 Interpretación del análisis
        interpretation = {
            "summary": "El texto analiza realidades hipersticiosas desde diferentes enfoques narrativos.",
            "detailed": [
                "✅ **Escenarios catastróficos:** Se enfatiza una visión apocalíptica del futuro." if "catastrofismo" in detected_terms else None,
                "✅ **Elementos conspirativos:** Se presentan teorías sobre control global o manipulación." if "conspiraciones" in detected_terms else None,
                "✅ **Estrategias psicológicas:** Se insinúa manipulación mental o falta de pensamiento crítico." if "psicologismos" in detected_terms else None,
                "✅ **Futurismo mesiánico:** Se plantean escenarios de transformación, salvación o ascensión." if "futurismo_mesianico" in detected_terms else None,
            ]
        }
        interpretation["detailed"] = [x for x in interpretation["detailed"] if x]

        return {
            "original_text": input_text.text,
            "detected_terms": detected_terms,
            "referential_analysis": referential_analysis,
            "semantic_relationships": semantic_relationships,
            "semantic_score": {"total": semantic_score, "level": score_level},
            "text_style": text_style,
            "interpretation": interpretation,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el análisis: {str(e)}")

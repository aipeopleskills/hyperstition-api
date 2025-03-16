import pytest
from httpx import AsyncClient
from app.main import app
from app.config.settings import settings

TEST_TEXT = "El neurocapitalismo acelera el colapso geopolítico mediante algoritmos predictivos."

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_syntactic_analysis(client):
    """Prueba el análisis sintáctico integrado en la respuesta"""
    response = await client.post(
        "/hyperstition/analyze",
        json={"text": TEST_TEXT}
    )
    
    assert response.status_code == 200
    json_response = response.json()
    
    # Verificación básica de estructura sintáctica
    assert "syntax" in json_response
    assert isinstance(json_response["syntax"], dict)
    
    # Validación de campos específicos
    syntax_data = json_response["syntax"]
    assert "complexity" in syntax_data
    assert isinstance(syntax_data["complexity"], dict)
    
    # Verificación de valores numéricos
    assert syntax_data["complexity"]["score"] > 0
    assert syntax_data["complexity"]["subordinate_clauses"] >= 0
    assert syntax_data["complexity"]["depth_score"] > 0

@pytest.mark.asyncio
async def test_full_analysis_structure(client):
    """Prueba la estructura completa de la respuesta"""
    response = await client.post(
        "/hyperstition/analyze",
        json={"text": TEST_TEXT}
    )
    
    assert response.status_code == 200
    json_response = response.json()
    
    # Campos obligatorios
    required_fields = {
        "hyperstition", 
        "semantics", 
        "syntax", 
        "risk_profile", 
        "discourse_style"
    }
    assert all(field in json_response for field in required_fields)
    
    # Validación de tipos
    assert isinstance(json_response["syntax"]["dependencies"], list)
    assert isinstance(json_response["risk_profile"]["level"], str)

@pytest.mark.asyncio
async def test_error_handling(client):
    """Prueba el manejo de errores con input inválido"""
    response = await client.post(
        "/hyperstition/analyze",
        json={"invalid_field": "texto mal formado"}
    )
    
    assert response.status_code == 422
    assert "detail" in response.json()

@pytest.mark.asyncio
async def test_empty_input(client):
    """Prueba el comportamiento con texto vacío"""
    response = await client.post(
        "/hyperstition/analyze",
        json={"text": ""}
    )
    
    assert response.status_code == 400
    assert "text" in response.json()["detail"].lower()
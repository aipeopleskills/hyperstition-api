from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Hyperstition API",
    root_path="/",
    docs_url="/docs",
    redoc_url=None
)

# Middleware de filtrado con manejo de errores
@app.middleware("http")
async def filter_invalid_requests(request: Request, call_next):
    try:
        user_agent = request.headers.get("User-Agent", "")
        allowed_patterns = ["Mozilla", "PostmanRuntime", "curl", "Swagger-Codegen", "GitHub-Hookshot"]
        
        if not request.headers.get("Host"):
            raise HTTPException(status_code=400, detail="Missing Host header")
            
        if not any(pattern in user_agent for pattern in allowed_patterns):
            raise HTTPException(status_code=403, detail="Forbidden User-Agent")
        
        return await call_next(request)
    except Exception as e:
        print(f"Error en middleware: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Endpoint /health con manejo de errores
@app.get("/health", include_in_schema=False)
def health_check():
    try:
        return {"status": "operational"}
    except Exception as e:
        print(f"Error en /health: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Configuración de Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="debug"
    )
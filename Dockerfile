# Base image oficial de Python
FROM python:3.12-slim

# 1. Instalar dependencias del sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 2. Crear usuario no-root y directorio de trabajo
RUN useradd -m -U appuser && \
    mkdir -p /app && \
    chown appuser:appuser /app

WORKDIR /app
USER appuser

# 3. Configurar variables de entorno
ENV PATH="/home/appuser/.local/bin:${PATH}" \
    PYTHONPATH="/app" \
    PYTHONUNBUFFERED=1

# 4. Copiar e instalar dependencias
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# 5. Copiar código de la aplicación
COPY --chown=appuser:appuser . .

# 6. Comando de ejecución (con proxy-headers para Codespaces)
CMD ["uvicorn", "app.main:app", \
    "--host", "0.0.0.0", \
    "--port", "8000", \
    "--proxy-headers", \
    "--root-path", "/", \
    "--forwarded-allow-ips", "*", \
    "--no-use-colors"]  # Evita conflictos con el túnel
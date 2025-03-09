# # Base image oficial de Python
FROM python:3.12-slim

# 1. Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 2. Instalar pip y dependencias de Python
RUN python -m ensurepip --default-pip && \
    pip install --no-cache-dir --upgrade pip setuptools wheel

# 3. Crear usuario no-root y directorio de trabajo
RUN useradd -m -U appuser && \
    mkdir -p /app && \
    chown appuser:appuser /app

WORKDIR /app

# 4. Configurar variables de entorno
ENV PATH="/home/appuser/.local/bin:${PATH}" \
    PYTHONPATH="/app" \
    PYTHONUNBUFFERED=1

# 5. Copiar e instalar dependencias como root para evitar problemas de permisos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt uvicorn fastapi
RUN pip install --no-cache-dir -r requirements.txt uvicorn fastapi aioredis


# 6. Cambiar al usuario no-root
USER appuser

# 7. Copiar el código de la aplicación
COPY --chown=appuser:appuser . .

# 8. Comando de ejecución (con exec para mejor manejo de señales)
CMD exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --proxy-headers --forwarded-allow-ips "*"

# Base image oficial de Python
FROM python:3.12-slim

# 1. Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 2. Instalar pip y dependencias de Python
RUN python -m ensurepip --default-pip && \
    pip install --no-cache-dir --upgrade pip setuptools wheel

# 3. Instalar PyTorch y Transformers (Hugging Face)
RUN pip install --no-cache-dir torch torchvision torchaudio transformers

# 4. Crear usuario no-root y directorio de trabajo
RUN useradd -m -U appuser && \
    mkdir -p /app && \
    chown appuser:appuser /app

WORKDIR /app

# 5. Configurar variables de entorno
ENV PATH="/home/appuser/.local/bin:${PATH}" \
    PYTHONPATH="/app" \
    PYTHONUNBUFFERED=1 \
    APP_PORT=8000  

# Se puede cambiar el puerto en tiempo de ejecución con:
# docker run -e APP_PORT=9000

# 6. Copiar dependencias y optimizar caché
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 7. Cambiar al usuario no-root
USER appuser

# 8. Copiar el código de la aplicación
COPY --chown=appuser:appuser . .

# 9. Comando de ejecución optimizado con exec para mejor manejo de señales
CMD exec uvicorn app.main:app --host 0.0.0.0 --port $APP_PORT --proxy-headers --forwarded-allow-ips "*"

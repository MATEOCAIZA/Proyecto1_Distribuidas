# ─────────────────────────────────────────────
# Stage 1: Builder — instala dependencias
# ─────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app

# Instalar dependencias del sistema necesarias para bcrypt y Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt


# ─────────────────────────────────────────────
# Stage 2: Runner — imagen final liviana
# ─────────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# Copiar dependencias instaladas del builder
COPY --from=builder /install /usr/local

# Copiar código fuente
COPY . .

# Crear carpeta de uploads (archivos multimedia)
RUN mkdir -p uploads

# Puerto que expone el servidor
EXPOSE 3001

# Variables de entorno por defecto (sobreescribibles en Render)
ENV PORT=3001
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Comando de inicio con eventlet (requerido por Flask-SocketIO)
CMD ["python", "src/app.py"]

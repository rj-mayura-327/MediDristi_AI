# ============================================================
# MediDrishti AI — Dockerfile
# A Streamlit-based medical report analyzer powered by AI
# ============================================================

# ---------- Stage 1: Base image ----------
FROM python:3.11-slim AS base

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ---------- Stage 2: System dependencies ----------
# EasyOCR and OpenCV require certain system libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# ---------- Stage 3: Application setup ----------
WORKDIR /app

# Install Python dependencies first (leverages Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY app.py .
COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY utils/ ./utils/
COPY assets/ ./assets/
COPY .env.example ./.env.example

# Create directories that the app may need at runtime
RUN mkdir -p uploads temp

# ---------- Stage 4: Runtime configuration ----------
# Expose the default Streamlit port
EXPOSE 8501

# Streamlit configuration — disable CORS/XSRF for container use,
# bind to all interfaces so the container is reachable
ENV STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Health check to verify the app is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" || exit 1

# Launch Streamlit
ENTRYPOINT ["streamlit", "run", "app.py"]

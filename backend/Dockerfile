# Use multi-stage build for a smaller final image
# Stage 1: Build dependencies
FROM python:3.9-slim AS builder

WORKDIR /app

# Install system dependencies for gmpy2
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libgmp-dev \
    libmpfr-dev \
    libmpc-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies and create virtual environment
RUN pip install --no-cache-dir --upgrade pip && \
    pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt

# Stage 2: Run-time image
FROM python:3.9-slim

WORKDIR /app

# Install runtime system dependencies for gmpy2
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgmp10 \
    libmpfr6 \
    libmpc3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Install production dependencies
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* && \
    rm -rf /wheels

# Copy application code
COPY . .

# Expose port for FastAPI
EXPOSE 8000

# Command to run the FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 
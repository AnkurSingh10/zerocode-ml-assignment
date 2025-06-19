# Use a minimal Python base image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy the requirements first (for layer caching)
COPY requirements.txt .

# Install system-level dependencies and Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
 && rm -rf /var/lib/apt/lists/* \
 && pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY Embeddings/ ./Embeddings/

# Set environment variable to avoid bytecode generation
ENV PYTHONDONTWRITEBYTECODE 1

# Set environment variable to buffer stdout
ENV PYTHONUNBUFFERED 1

# Expose port
EXPOSE 8000

# Run the FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

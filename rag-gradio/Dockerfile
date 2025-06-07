# Use official lightweight Python image
FROM python:3.10-slim

# Avoid Python writing .pyc files and force stdout/stderr flushing
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set environment variables for external APIs
ENV TOKENIZERS_PARALLELISM=false

# Recommended to pass these as runtime env variables, not hardcoded
# ENV REPLICATE_API_TOKEN=your_replicate_api_token_here
# ENV COHERE_API_KEY=your_cohere_api_key_here

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    git \
    poppler-utils \
    tesseract-ocr \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --default-timeout=100 --retries=10 --no-cache-dir -r requirements.txt

# Copy app files into the container
COPY . .

# Gradio runs on port 7860 by default
EXPOSE 7860

# Start the app
CMD ["python", "app.py"]

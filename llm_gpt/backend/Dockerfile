# Use official Python 3.9.16 base image
FROM python:3.9.16-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code

# Install system dependencies required by unstructured and NLTK
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libmagic1 \
    poppler-utils \
    tesseract-ocr \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies (nltk included here)
RUN pip install --upgrade pip && pip install -r requirements.txt

# Pre-install NLTK data to avoid runtime issues
ENV NLTK_DATA=/usr/share/nltk_data
RUN mkdir -p $NLTK_DATA && \
    python -m nltk.downloader -d $NLTK_DATA punkt averaged_perceptron_tagger

# Copy application files
COPY . /code/

# Expose port
EXPOSE 8000

# Run the app
CMD ["gunicorn", "main:app", \
     "--chdir", "/code/app", \
     "-k", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--timeout", "300"]


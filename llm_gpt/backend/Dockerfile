# Use official Python 3.9.16 base image
FROM python:3.9.16-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency list
COPY requirements.txt .

COPY .env .env

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy project files
COPY . .

# Expose port uvicorn will run on
EXPOSE 8000

# Default command to run the app
CMD ["uvicorn", "--app-dir=./app", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

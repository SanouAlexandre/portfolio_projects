# Use official Python 3.8 image
FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Copy requirements first (to leverage Docker cache)
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html


# Copy project files
COPY . .

# Expose port Flask runs on
EXPOSE 5000

# Set default command to run the Flask app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]

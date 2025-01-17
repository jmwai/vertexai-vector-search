# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /code/

# Collect static files (optional, if you use static files)
# RUN python manage.py collectstatic --noinput
ENV GOOGLE_APPLICATION_CREDENTIALS=gcredentials.json
# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

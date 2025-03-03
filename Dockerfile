# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Prevent Python from writing pyc files to disk and enable stdout/stderr logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies (adjust as needed)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements.txt first to leverage Docker layer caching
COPY requirements.txt /app/

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose the default Django port
EXPOSE 4000

# Run the Django development server (adjust for production)
CMD ["python", "manage.py", "runserver", "0.0.0.0:4000"]

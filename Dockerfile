# Use a lightweight Python image
FROM python:slim

# Prevent .pyc files & ensure unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working dir inside container
WORKDIR /app

# Install system dependencies (e.g., LightGBM)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy project code (excluding .dockerignore items)
COPY . .

# Install Python deps
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e .

# Expose port (optional)
EXPOSE 5000

# Default: Run your app (optional)
CMD ["python", "application.py"]

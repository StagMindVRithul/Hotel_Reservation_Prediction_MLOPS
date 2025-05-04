# Use a lightweight Python image
FROM python:slim

# Set environment variables to prevent .pyc files & ensure Python output is not buffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (e.g., for LightGBM)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the entire project code into /app
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e .

# Optional: Set default GOOGLE_APPLICATION_CREDENTIALS path (matches your Jenkins run command)
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/gcp-key.json"

# Train the model (if this needs GCP access, the mounted key will help)
RUN python pipeline/training_pipeline.py

# Expose the port (e.g., if you are using Flask or FastAPI)
EXPOSE 5000

# Default command: Run the application
CMD ["python", "application.py"]

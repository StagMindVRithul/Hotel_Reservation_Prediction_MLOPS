# Use a lightweight Python image
FROM python:3.11-slim  

# Set environment variables to prevent .pyc files & ensure unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy GCP key before installing anything (best practice)
COPY gcp_key.json ./gcp_key.json
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/gcp_key.json"

# Install system dependencies required by LightGBM
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the application code
COPY . .

# Install Python dependencies (this assumes you have setup.py for editable mode)
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -e .

# Train the model before running the application
RUN python pipeline/training_pipeline.py

# Expose the port that Flask will run on
EXPOSE 5000

# Command to run the app
CMD ["python", "application.py"]

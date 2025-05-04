FROM python:3.11-slim  

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# DO NOT COPY gcp_key.json here!

# Install system dependencies required by LightGBM
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the application code
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -e .

# Train the model (optional)
RUN python pipeline/training_pipeline.py

# Expose the port
EXPOSE 5000

# CMD runs app (auth will happen at runtime!)
CMD ["python", "application.py"]

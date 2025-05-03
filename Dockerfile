FROM python:slim

# Set environment variables to avoid Python writing .pyc files and buffering output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Update apt-get, install necessary packages, and clean up
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory content to /app in the container
COPY . .

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -e .

# Run the training pipeline script
RUN python pipeline/training_pipeline.py

# Expose port 5000 for the application
EXPOSE 5000

# Set the default command to run the application
CMD ["python", "application.py"]

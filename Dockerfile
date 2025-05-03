FROM python:slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set Google credentials env
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Copy Credentials File (use your actual file name here)
COPY /Users/rithul.v/Desktop/Hotel_Reservation_Project/shaped-manifest-457208-f6-00c80b4ae9f0.json /app/credentials.json

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Run GCP pipeline
RUN python pipeline/training_pipeline.py

EXPOSE 5000

CMD ["python", "application.py"]

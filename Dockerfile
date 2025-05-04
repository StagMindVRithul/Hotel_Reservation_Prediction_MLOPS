FROM python:slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ARG for credentials path
ARG GOOGLE_APPLICATION_CREDENTIALS_PATH

# Set the environment variable for the credentials file
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json

WORKDIR /app

# Install necessary libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the project files into the container
COPY . .

# Copy the credentials file from the build context into the container
COPY ${GOOGLE_APPLICATION_CREDENTIALS_PATH} /app/credentials.json

# Install the required Python dependencies
RUN pip install --no-cache-dir -e .

# Expose the port that the app will use
EXPOSE 5000

# Default command to run the application
CMD ["python", "application.py"]
FROM python:slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ARG for credentials path
ARG GOOGLE_APPLICATION_CREDENTIALS_PATH

# Set the environment variable for the credentials file
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json

WORKDIR /app

# Install necessary libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the project files into the container
COPY . .

# Copy the credentials file from the build context into the container
COPY ${GOOGLE_APPLICATION_CREDENTIALS_PATH} /app/credentials.json

# Install the required Python dependencies
RUN pip install --no-cache-dir -e .

# Expose the port that the app will use
EXPOSE 5000

# Default command to run the application
CMD ["python", "application.py"]

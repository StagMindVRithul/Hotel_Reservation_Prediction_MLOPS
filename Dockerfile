FROM python:slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1



# ARG

ARG GOOGLE_APPLICATION_CREDENTIALS_PATH
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json

WORKDIR /app



RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*



COPY . .



# Copy Credentials File

COPY ${GOOGLE_APPLICATION_CREDENTIALS_PATH} /app/credentials.json


# Installl 
RUN pip install --no-cache-dir -e .



# GCP işlemlerini bu aşamada yapma

RUN python pipeline/training_pipeline.py


#RUNNNN
EXPOSE 5000


#RUN
CMD ["python", "application.py"]
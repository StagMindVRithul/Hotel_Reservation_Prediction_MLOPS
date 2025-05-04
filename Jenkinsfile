pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "shaped-manifest-457208-f6"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
        IMAGE_NAME = "gcr.io/${GCP_PROJECT}/ml-project:${BUILD_NUMBER}"
    }

    stages {
        stage('Cloning Github repo to Jenkins') {
            steps {
                script {
                    echo 'Cloning Github repo to Jenkins............'
                    checkout scmGit(
                        branches: [[name: '*/main']], 
                        extensions: [], 
                        userRemoteConfigs: [[
                            credentialsId: 'github-token', 
                            url: 'https://github.com/StagMindVRithul/Hotel_Reservation_Prediction_MLOPS.git'
                        ]]
                    )
                }
            }
        }

        stage('Setting up Virtual Env and Installing Dependencies') {
            steps {
                script {
                    echo 'Setting up Virtual Env and Installing Dependencies............'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }

        stage('Building and Pushing Docker Image to GCR') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Building and Pushing Docker Image to GCR.............'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        
                        # Authenticate and configure Docker
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet
                        
                        # Build and push Docker image
                        docker build -t ${IMAGE_NAME} .
                        docker push ${IMAGE_NAME}
                        '''
                    }
                }
            }
        }

        stage('Run Training Pipeline') {
            steps {
                script {
                    echo 'Running Training Pipeline............'
                    sh '''
                    . ${VENV_DIR}/bin/activate
                    python pipeline/training_pipeline.py
                    '''
                }
            }
        }

        stage('Deploy to Google Cloud Run') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Deploying to Google Cloud Run.............'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}

                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}

                        gcloud run deploy ml-project \
                            --image=${IMAGE_NAME} \
                            --platform=managed \
                            --region=us-central1 \
                            --allow-unauthenticated
                        '''
                    }
                }
            }
        }
    }
}
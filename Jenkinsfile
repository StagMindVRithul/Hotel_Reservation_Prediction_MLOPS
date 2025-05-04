pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "shaped-manifest-457208-f6"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
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

        stage('Setting up our Virtual Environment and Installing Dependencies') {
            steps {
                script {
                    echo 'Setting up our Virtual Environment and Installing Dependencies............'
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
                withCredentials([string(credentialsId: 'gcp-key-json', variable: 'GCP_KEY_JSON')]) {
                    script {
                        echo 'Building and Pushing Docker Image to GCR.............'
                        sh '''
                            export PATH=$PATH:${GCLOUD_PATH}

                            # Authenticate using JSON key passed via env
                            echo "$GCP_KEY_JSON" > /tmp/gcp-key.json

                            gcloud auth activate-service-account --key-file=/tmp/gcp-key.json
                            gcloud config set project ${GCP_PROJECT}
                            gcloud auth configure-docker --quiet

                            docker build -t gcr.io/${GCP_PROJECT}/ml-project:latest .
                            docker push gcr.io/${GCP_PROJECT}/ml-project:latest 

                            # Cleanup
                            rm /tmp/gcp-key.json
                        '''
                    }
                }
            }
        }
    }
}

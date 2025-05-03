pipeline {
    agent any
    environment {
        GOOGLE_APPLICATION_CREDENTIALS = credentials('gcp-service-account')
    }
    stages {
        stage('Cloning Github Repo to Jenkins') {
            steps {
                echo 'Cloning Github Repo to Jenkins...............'
                checkout([$class: 'GitSCM',
                          branches: [[name: '*/main']],
                          userRemoteConfigs: [[
                              url: 'https://github.com/StagMindVRithul/Hotel_Reservation_Prediction_MLOPS.git',
                              credentialsId: 'github-token'
                          ]]
                ])
            }
        }

        stage('Run Python 3.12 & Install dependencies') {
            steps {
                echo 'Running in Python 3.12 Docker and Installing deps............'
                script {
                    sh '''
                    docker run --rm -v $(pwd):/app -w /app python:3.12 bash -c "
                        python -m venv venv &&
                        . venv/bin/activate &&
                        pip install --upgrade pip &&
                        pip install -e .
                    "
                    '''
                }
            }
        }

        stage('Building and Pushing Docker Image to GCR') {
            steps {
                echo 'Building and Pushing Docker Image to GCR..............'
                script {
                    sh '''
                    export PATH=$PATH:/var/jenkins_home/google-cloud-sdk/bin
                    gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
                    gcloud config set project shaped-manifest-457208-f6
                    gcloud auth configure-docker --quiet
                    docker build -t gcr.io/shaped-manifest-457208-f6/ml-project:latest .
                    docker push gcr.io/shaped-manifest-457208-f6/ml-project:latest
                    '''
                }
            }
        }
    }
}

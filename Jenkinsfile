pipeline {
    agent any

    environment {
        PROJECT_ID = "gke-python-ci-cd"
        REGION = "us-central1"
        REPO = "python-app-repo"
        IMAGE = "python-app"
        CLUSTER = "python-app-gke-cluster"
        ZONE = "us-central1-a"
    }
docker ps

    stages {

        stage('Checkout') {
            steps {
                git 'https://github.com/your-username/your-repo.git'
            }
        }

        stage('Authenticate GCP') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'KEY')]) {
                    sh '''
                    gcloud auth activate-service-account --key-file=$KEY
                    gcloud config set project $PROJECT_ID
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/$IMAGE:1.0 .
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                sh '''
                gcloud auth configure-docker $REGION-docker.pkg.dev -q
                docker push $REGION-docker.pkg.dev/$PROJECT_ID/$REPO/$IMAGE:1.0
                '''
            }
        }

        stage('Deploy to GKE') {
            steps {
                sh '''
                gcloud container clusters get-credentials $CLUSTER --zone $ZONE
                helm upgrade --install python-app ./python-app
                '''
            }
        }
    }
}

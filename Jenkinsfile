pipeline {
    agent any

    environment {
        PROJECT_ID = "python-app-deployment-demo"
        REGION     = "us-central1"
        REPO       = "python-app-repo"
        IMAGE      = "my-python-app"
        CLUSTER    = "python-app-gke-cluster"
        ZONE       = "us-central1-a"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-token',
                    url: 'https://github.com/Diwakara-KC/Vote-checker-app.git'
            }
        }

        stage('Verify Tools') {
            steps {
                bat '''
                echo Checking tools...
                docker --version
                gcloud --version
                helm version
                '''
            }
        }

        stage('Authenticate GCP') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'KEY')]) {
                    bat '''
                    gcloud auth activate-service-account --key-file="%KEY%"
                    gcloud config set project %PROJECT_ID%
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '''
                docker build -t %REGION%-docker.pkg.dev/%PROJECT_ID%/%REPO%/%IMAGE%:1.0 .
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                bat '''
                gcloud auth configure-docker %REGION%-docker.pkg.dev -q
                docker push %REGION%-docker.pkg.dev/%PROJECT_ID%/%REPO%/%IMAGE%:1.0
                '''
            }
        }

        stage('Deploy to GKE') {
            steps {
                bat '''
                gcloud container clusters get-credentials %CLUSTER% --zone %ZONE%
                helm upgrade --install python-app ./python-app
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully'
        }
        failure {
            echo '❌ Pipeline failed'
        }
    }
}

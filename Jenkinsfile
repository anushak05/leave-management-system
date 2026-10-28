
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'anushak05/leave-management'
        IMAGE_TAG = 'v2'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verify Project') {
            steps {
                bat '''
                    python --version
                    python -m pip install -r requirements.txt
                    python -c "from app import app; print('Flask V2 application loaded successfully')"
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '''
                    docker build -t %IMAGE_NAME%:%IMAGE_TAG% .
                '''
            }
        }

        stage('Test Docker Image') {
            steps {
                bat '''
                    docker image inspect %IMAGE_NAME%:%IMAGE_TAG%
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    bat '''
                        echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                        docker push %IMAGE_NAME%:%IMAGE_TAG%
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Version 2 Jenkins Pipeline Completed Successfully!'
        }

        failure {
            echo 'Version 2 Jenkins Pipeline Failed. Check Console Output.'
        }

        always {
            bat 'docker logout'
        }
    }
}

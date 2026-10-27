
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verify Docker') {
            steps {
                bat 'docker --version'
                bat 'docker info'
            }
        }

        stage('Build V1 Docker Image') {
            steps {
                bat 'docker build -t leave-management:v1 .'
            }
        }

        stage('Verify Image') {
            steps {
                bat 'docker image inspect leave-management:v1'
            }
        }
    }
}

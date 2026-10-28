
pipeline {
    agent any

    environment {
    IMAGE_NAME = 'anushak05/leave-management'
    IMAGE_TAG = 'v2'
    DOCKER_HOST = 'npipe:////./pipe/dockerDesktopLinuxEngine'
    DOCKER_CONTEXT = 'default'
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
                    if not exist app.py exit /b 1
                    if not exist requirements.txt exit /b 1
                    if not exist Dockerfile exit /b 1
                    if not exist templates\\index.html exit /b 1
                    if not exist templates\\admin.html exit /b 1
                    echo Version 2 project files verified successfully
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
                    docker run --rm %IMAGE_NAME%:%IMAGE_TAG% python -c "from app import app; assert any(rule.rule == '/admin' for rule in app.url_map.iter_rules()); print('Flask V2 admin route verified successfully')"
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
            echo 'Version 2 pipeline execution finished.'
        }
    }
}

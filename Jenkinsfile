
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'anushak05/leave-management'
        IMAGE_TAG = 'v2'
        DOCKER_HOST = 'npipe:////./pipe/dockerDesktopLinuxEngine'
        DOCKER_CONTEXT = 'default'
    }

    options {
        skipDefaultCheckout(true)
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
                    @echo off
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
                    @echo off
                    docker build -t %IMAGE_NAME%:%IMAGE_TAG% .
                    if errorlevel 1 exit /b 1

                    echo Version 2 Docker image built successfully
                '''
            }
        }

        stage('Test Docker Image') {
            steps {
                bat '''
                    @echo off
                    docker run --rm %IMAGE_NAME%:%IMAGE_TAG% python -c "from app import app; assert any(rule.rule == '/admin' for rule in app.url_map.iter_rules()); print('Flask V2 admin route verified successfully')"

                    if errorlevel 1 exit /b 1

                    echo Version 2 Docker image test passed
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
                    withEnv(['DOCKER_CONFIG=.docker-jenkins']) {
                        bat '''
                            @echo off
                            echo Logging in to Docker Hub...

                            echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin

                            if errorlevel 1 (
                                echo Docker Hub login failed
                                exit /b 1
                            )

                            echo Docker Hub login successful

                            docker push %IMAGE_NAME%:%IMAGE_TAG%

                            if errorlevel 1 (
                                echo Docker image push failed
                                exit /b 1
                            )

                            echo Version 2 image pushed successfully
                        '''
                    }
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
            withEnv(['DOCKER_CONFIG=.docker-jenkins']) {
                bat(returnStatus: true, script: '''
                    @echo off
                    docker logout >nul 2>&1
                ''')
            }

            dir('.docker-jenkins') {
                deleteDir()
            }

            echo 'Version 2 pipeline execution finished.'
        }
    }
}

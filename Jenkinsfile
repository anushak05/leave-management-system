
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'anushak05/leave-management'
        IMAGE_TAG = 'v3'
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

        stage('Verify V3 Project') {
            steps {
                bat '''
                    @echo off
                    if not exist app.py exit /b 1
                    if not exist requirements.txt exit /b 1
                    if not exist Dockerfile exit /b 1
                    if not exist templates\\index.html exit /b 1
                    if not exist templates\\admin.html exit /b 1
                    echo Version 3 project files verified
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '''
                    @echo off
                    docker build -t %IMAGE_NAME%:%IMAGE_TAG% .
                    if errorlevel 1 exit /b 1
                    echo Version 3 Docker image built successfully
                '''
            }
        }

        stage('Test V3 Reject Feature') {
            steps {
                bat '''
                    @echo off
                    docker run --rm %IMAGE_NAME%:%IMAGE_TAG% python -c "from app import app; c=app.test_client(); assert c.get('/').status_code == 200; assert c.get('/admin').status_code == 200; assert any(r.rule.startswith('/reject/') and 'POST' in r.methods for r in app.url_map.iter_rules()); print('Version 3 pages and Reject route verified')"
                    if errorlevel 1 exit /b 1
                    echo Version 3 Docker test passed
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
                        powershell '''
                            $ErrorActionPreference = "Stop"

                            Write-Host "Logging in to Docker Hub..."

                            $token = $env:DOCKER_PASS.Trim()
                            $token | docker login --username $env:DOCKER_USER --password-stdin

                            if ($LASTEXITCODE -ne 0) {
                                throw "Docker Hub login failed"
                            }

                            Write-Host "Docker Hub login successful"

                            docker push "$($env:IMAGE_NAME):$($env:IMAGE_TAG)"

                            if ($LASTEXITCODE -ne 0) {
                                throw "Docker image push failed"
                            }

                            Write-Host "Version 3 image pushed successfully"
                        '''
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Version 3 Jenkins Pipeline Completed Successfully!'
        }

        failure {
            echo 'Version 3 Jenkins Pipeline Failed. Check Console Output.'
        }

        always {
            withEnv(['DOCKER_CONFIG=.docker-jenkins']) {
                bat(
                    returnStatus: true,
                    script: 'docker logout >nul 2>&1'
                )
            }

            dir('.docker-jenkins') {
                deleteDir()
            }

            echo 'Version 3 pipeline execution finished.'
        }
    }
}

pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Environment Check') {
            steps {
                echo 'Checking build environment...'
                sh 'git --version'
                sh 'docker --version'
                sh 'docker compose version'
            }
        }

        stage('Prepare Environment') {
            steps {
                echo 'Preparing CI environment...'
                sh 'cp .env.example .env'
            }
        }

        stage('Validate Docker Compose') {
            steps {
                echo 'Validating Docker Compose configuration...'
                sh 'docker compose config'
            }
        }

        stage('Build Application') {
            steps {
                echo 'Building Docker application...'
                sh 'docker compose build'
            }
        }

    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check console output.'
        }

        always {
            echo 'Pipeline execution completed.'
        }
    }
}

stage('Automated Tests') {
    steps {
        echo 'Running API Automated Tests...'

        sh '''
            python3 --version
            python3 -m unittest discover -s tests -v
        '''
    }
}

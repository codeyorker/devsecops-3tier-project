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
    }
}

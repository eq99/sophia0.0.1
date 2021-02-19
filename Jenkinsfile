pipeline {
    agent none
    stages {
        stage('build') {
            agent { docker { image 'python:3.8' } }
            steps {
                sh 'python --version'
            }
        }
    }
}
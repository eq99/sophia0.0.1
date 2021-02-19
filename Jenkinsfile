pipeline {
    agent { docker { image 'python:3.8' } }
    environment {
        VERSION = '0.0.1'
    }
    stages {
        stage('build') {
            steps {
                sh 'docker build -t sophia:${VERSION} .'
            }
        }
        stage('run'){
            steps {
                sh 'docker run --name sophia --rm -d -p 80:80 sophia:${VERSION}'
            }
        }
    }
}
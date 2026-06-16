pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/SagarSahoo31/SmartChef-AI.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t smartchef .'
            }
        }

        stage('Stop Existing Container') {
            steps {
                bat 'docker stop smartchef-container'
                bat 'docker rm smartchef-container'
            }
        }

        stage('Run Container') {
            steps {
                bat 'docker run -d --name smartchef-container -p 5000:5000 smartchef'
            }
        }

    }
}
pipeline {
  agent any

  stages {
    stage('Build Docker Image') {
      steps {
        script {
          def dockerapp = docker.build("rickdevops/chaos-api:${env.BUILD_ID}", "-f Dockerfile .")
          env.IMAGE_ID = dockerapp.id
        }
      }
    }

    stage('Push') {
      steps {
        script {
          docker.withRegistry('https://registry.hub.docker.com', 'dockerhub') {
            docker.image(env.IMAGE_ID).push('latest')
            docker.image(env.IMAGE_ID).push("${env.BUILD_ID}")
          }
        }
      }
    }

    stage('Deploy') {
      steps {
        sh 'echo "Apply"'
      }
    }
  }
}

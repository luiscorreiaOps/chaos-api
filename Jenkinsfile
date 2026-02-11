pipelane{
  agent any

  stages {
      stage('Build Docker Image') {
          steps {
              sh 'echo' "Executando docker Build"
          }
      }
      stage('Push') {
          steps {
              sh'echo' "Executando docker Push"
          }
      }
      stage('Deploy') {
          steps {
              sh'echo' "Apply"
          }
      }
  }
}

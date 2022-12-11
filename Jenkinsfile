pipeline {
  environment {
    imagename = "christhai/telegram-bot"
    registryCredential = 'jenkins'
    dockerImage = ''
  }
  agent any
  stages {
    stage('Cloning Git') {
      steps {
        git([url: 'https://github.com/christhai/3commas-telegram-bot-trader.git', branch: 'jenkins', credentialsId: 'jenkins-hai'])
 
      }
    }
    stage('Building image') {
      steps{
        script {
          dockerImage = docker.build imagename
        }
      }
    }
    stage ('Pull image to local') { // take that image and push to artifactory
      steps {
          rtDockerPull(
              serverId: "jfrog-platform",
              image: "10.0.0.87:8081/docker-local/nginx:latest",
              sourceRepo: 'docker-local'
          )
      }
  }
    stage ('Push image to Artifactory') { // take that image and push to artifactory
      steps {
          rtDockerPush(
              serverId: "jfrog-platform",
              image: "10.0.0.87:8081/docker-local/nginx:latest",
              targetRepo: 'docker-local', 
              properties: 'status=stable'
          )
      }
  }
    stage('Remove Unused docker image') {
      steps{
        sh "docker rmi $imagename:$BUILD_NUMBER"
         sh "docker rmi $imagename:latest"
 
      }
    }
  }
}

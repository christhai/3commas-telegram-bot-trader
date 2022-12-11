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
    stage('Push docker registry latest') {
      steps {
        container('builder') {
          withCredentials(
            [usernamePassword(
              credentialsId: 'docker-registry-credentials',
              passwordVariable: 'DOCKER_PASSWORD',
              usernameVariable: 'DOCKER_LOGIN')]
          ){
            echo 'Docker Login to Talend registry'
            sh '''
              #! /bin/bash
              set +x
              echo $DOCKER_PASSWORD | docker login http://10.0.0.87:8081 -u $DOCKER_LOGIN --password-stdin
            '''
          }
          sh 'docker tag nginx  10.0.0.87:8081/docker-local/nginx:latest'
          retry(3) {
            sh 'docker push 10.0.0.87:8081/docker-local/nginx'
          }
        }
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

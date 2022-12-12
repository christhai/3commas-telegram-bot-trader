pipeline {
  environment {
    imagename = "docker-local/christhai/telegram-bot"
    registryCredential = 'jenkins'
    dockerImage = ''
    artifactory = '10.0.0.87:8081'
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
    
    stage('Pushing image') {
      steps{
        script {
          docker.withRegistry('http://10.0.0.87:8081', 'docker-registry-credentials') {
            dockerImage.push('latest')
          }
        }
      }
    }
    
    stage('Push docker registry latest') {
      steps {
        script {
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
              echo $DOCKER_PASSWORD | docker login http://${artifactory} -u $DOCKER_LOGIN --password-stdin
            '''
          }
          sh 'docker tag $imagename  ${artifactory}/${imagename}:latest'
          retry(3) {
            sh 'docker push ${artifactory}/$imagename:latest'
          }
        }
      }
    }
    stage('Remove Unused docker image') {
      steps{
         sh "docker rmi $imagename:latest"
 
      }
    }
  }
}

pipeline {
  agent none
  options { skipDefaultCheckout() }
  stages {
    stage('Build') {
      agent {
        docker {
          args '-v /var/jenkins_home/RC_Car/conan/profiles/:/home/conan/profiles/ --network docker_ci_network'
          image 'conanio/gcc8-armv7hf'
        }

      }
      steps {
        echo 'TEST'
      }
    }

  }
}
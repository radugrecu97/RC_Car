pipeline {
  agent any
  options { skipDefaultCheckout() }
  stages {
    stage('Build') {
      agent {
        docker {
          args '-v /var/jenkins_home/RC_Car/conan/profiles/:/home/conan/profiles/ --network docker_ci_network'
          image 'conanio/gcc8-armv7hf'
        }
        options { skipDefaultCheckout() }
      }
      steps {
        echo "TEST"
      }
    }
  }
}
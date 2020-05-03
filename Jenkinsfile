pipeline {
  agent {
    docker {
      image 'conanio/gcc8-armv7hf'
      args '-v /var/jenkins_home/RC_Car/conan/profiles/:/home/conan/profiles/ --network docker_ci_network'
    }

  }
  stages {
    stage('') {
      steps {
        echo 'Checked out'
      }
    }

  }
}
pipeline {
  agent {
    docker {
      image 'conanio/gcc8-armv7hf'
      args '-v /var/jenkins_home/RC_Car/conan/profiles/:/home/conan/profiles/ --network docker_ci_network'
    }

  }
  stages {
    stage('Build') {
      agent any
      steps {
        script {
          def ARTIFACTORY_NAME = "art-01"
          def ARTIFACTORY_REPO = "conan-local"

          def MAX_BUILDS = 10
          def MAX_DAYS = 7

          def server = Artifactory.server ARTIFACTORY_NAME
          def client = Artifactory.newConanClient(userHome: "${env.WORKSPACE}/conan_home".toString())
          def serverName = client.remote.add server: server, repo: ARTIFACTORY_REPO


          String command = "create . radugrecu97/experimental -pr ./ci/conan/profiles/rpi_gcc8 --build=missing"
          client.run(command: command)
        }

      }
    }

    stage('Test') {
      steps {
        node(label: 'rpi-slave') {
          sh 'ls -la'
        }

      }
    }

  }
}
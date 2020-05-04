pipeline {
  agent any
  stages {
    stage('Build') {
      agent {
        docker {
          args '-v /var/jenkins_home/RC_Car/conan/profiles/:/home/conan/profiles/ --network docker_ci_network'
          image 'conanio/gcc8-armv7hf'
        }

      }
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
      parallel {
        stage('Google Test') {
          steps {
            script {
              withEnv(["WORKSPACE=/var/jenkins_home/workspace/RC_Car_Pipeline_master@2"]) {
                script {
                  sshPublisher(
                    continueOnError: false, failOnError: true,
                    publishers: [
                      sshPublisherDesc(
                        configName: "RPi_Testing",
                        verbose: true,
                        transfers: [
                          sshTransfer(
                            sourceFiles: "conan_home/.conan/data/RC_Car/0.1/radugrecu97/experimental/package/*/bin/*",
                            flatten: true,
                            cleanRemote: true,
                            remoteDirectory: "RC_Car_Pipeline_master/bin",
                          ),
                          sshTransfer(
                            execCommand: "chrpath -r RC_Car_Pipeline_master/lib RC_Car_Pipeline_master/bin/*"
                          ),
                          sshTransfer(
                            sourceFiles: "../RC_Car_Pipeline_master@2/conan_home/.conan/data/*/*/_/_/package/*/lib/*",
                            flatten: true,
                            cleanRemote: true,
                            remoteDirectory: "RC_Car_Pipeline_master/lib",
                          ),
                          sshTransfer(
                            execCommand: "chmod u+x RC_Car_Pipeline_master/bin/*"
                          ),
                          sshTransfer(
                            execCommand: "RC_Car_Pipeline_master/bin/Motor_test --gtest_output=xml:RC_Car_Pipeline_master/reports/gtestresults.xml"
                          ),
                        ]
                      )
                    ]
                  )
                }
              }
            }

          }
        }

        stage('Visualize GTest') {
          steps {
            echo 'Visualize'
          }
        }

      }
    }

  }
}
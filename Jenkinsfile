pipeline {
  agent {
          label {
              label "master"
          }
      }
  options {
          skipDefaultCheckout ()
      }
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
        stage('Google Test') {
          steps {
            script {
              dir('../RC_Car_Pipeline_master@2') {
                script {
                  sshPublisher(
                    continueOnError: false, failOnError: true,
                    publishers: [
                      sshPublisherDesc(
                        configName: "RPi_Testing",
                        verbose: true,
                        transfers: [
                          // copy binaries
                          sshTransfer(
                            sourceFiles: "conan_home/.conan/data/RC_Car/0.1/radugrecu97/experimental/package/*/bin/",
                            flatten: true, // removes the directory prefix to file so only the file is copied and not the folders tree to it as well
                            cleanRemote: true, // clean the remote directory below before copying
                            remoteDirectory: "RC_Car_Pipeline_master/bin",
                          ),
                          // copy shared libraries
                          sshTransfer(
                            sourceFiles: "conan_home/.conan/data/*/*/_/_/package/*/lib/*",
                            flatten: true,
                            cleanRemote: true,
                            remoteDirectory: "RC_Car_Pipeline_master/lib",
                          ),
                          // make binaries executable
                          sshTransfer(
                            execCommand: "chmod u+x /home/jenkins/jenkins_slave/workspace/RC_Car_Pipeline_master/bin/*"
                          ),
                          // change library path for shared libraries
                          sshTransfer(
                            execCommand: "chrpath -r /home/jenkins/jenkins_slave/workspace/RC_Car_Pipeline_master/lib /home/jenkins/jenkins_slave/workspace/RC_Car_Pipeline_master/bin/*"
                          ),
                          // clean reports folder
                          sshTransfer(
                            execCommand: "rm -rf /home/jenkins/jenkins_slave/workspace/RC_Car_Pipeline_master/reports"
                          ),
                          // run Google Test and save xUnit report
                          sshTransfer(
                            execCommand: "/home/jenkins/jenkins_slave/workspace/RC_Car_Pipeline_master/bin/Motor_test --gtest_output=xml:/home/jenkins/jenkins_slave/workspace/RC_Car_Pipeline_master/reports/gtestresults.xml"
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
            script {
              dir('../RC_Car_Pipeline_master@2') {
                script {
                  load "ci/pipeline/copy_gtest_report.groovy"
                }
              }
            }

          }
        }
    }

  }
}
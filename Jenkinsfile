  def ARTIFACTORY_NAME = "art-01"
  def ARTIFACTORY_REPO = "conan-local"

  def server = Artifactory.server ARTIFACTORY_NAME
  def client
  def serverName

pipeline {
  // run Docker agent from Dockerfile because sshpass is required
  agent {
    dockerfile {
      dir 'ci/Docker/Dockerfiles/conan'
      args '-v /var/jenkins_home/RC_Car/conan/profiles/:/home/conan/profiles/ --network docker_ci_network'
    }
  }

  stages {

      stage('Get dependencies & Build') {
        steps {
          script {
            sh 'printenv'
            sh 'pwd'
            client = Artifactory.newConanClient(userHome: "${env.WORKSPACE}/conan_home".toString())
            String command = "create . radugrecu97/experimental -pr ./ci/conan/profiles/rpi_gcc8 --build=missing"
            client.run(command: command)
          }
        }
      }

      stage('Google Test') {
        steps {
          script {
            dir('../RC_Car_Pipeline_master@2') {
              sshPublisher(
                continueOnError: false,
                failOnError: true,
                publishers: [
                  sshPublisherDesc(
                    // configName is acquired from Manage Jenkins > Configure System > Publish over SSH
                    configName: "RPi_Testing",
                    verbose: true,
                    continueOnError: false,
                    failOnError: true,
                    transfers: [
                      // copy binaries
                      sshTransfer(
                        sourceFiles: "conan_home/.conan/data/RC_Car/0.1/radugrecu97/experimental/package/*/bin/",
                        flatten: true, // removes the directory prefix to file so only the file is copied and not the folders tree to it as well
                        cleanRemote: true, // clean the remote directory below before copying
                        remoteDirectory: "RC_Car_Pipeline_master/bin", // appends to the remote directory specified in the configuration
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
                        execCommand: "chmod u+x /home/jenkins/jenkins_slave/workspace/RC_Car_Pipeline_master/bin/*" // run command in remote host
                      ),
                      // change library path for shared libraries
                      sshTransfer(
                        execCommand: "chrpath -r /home/jenkins/jenkins_slave/workspace/RC_Car_Pipeline_master/lib /home/jenkins/jenkins_slave/workspace/RC_Car_Pipeline_master/bin/*"
                      ),
                      // clean reports folder in remote host
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

      stage('Transfer GTest') {
        steps {
          script {
            load "ci/pipeline/copy_gtest_report.groovy"
          }
        }
      }

      stage('Visualize GTest') {
        steps {
          script {
            xunit (
              tools: [ GoogleTest(pattern: 'gtestresults.xml') ]
            )
          }
        }
      }

      stage("Upload artifacts") {
        steps {
          script {
            client = Artifactory.newConanClient(userHome: "${env.WORKSPACE}/conan_home".toString())
            serverName = client.remote.add server: server, repo: ARTIFACTORY_REPO
            String command = "upload RC_Car/*@radugrecu97/experimental --all -r ${serverName} --confirm"
            def b = client.run(command: command)
            b.env.collect()
            b.number = "v0.${BUILD_NUMBER}" // BUILD_NUMBER is a Jenkins environment variable
            server.publishBuildInfo b
            echo "RESULT: ${currentBuild.result}"
            currentBuild.result = "SUCCESS"
            echo "RESULT: ${currentBuild.result}"
          }
        }
      }

  }

  post {
    success {
        echo "RESULT: ${currentBuild.result}"
        echo "Success"
    }
    failure {
        echo "RESULT: ${currentBuild.result}"
        echo "Failure"
    }
  }

}
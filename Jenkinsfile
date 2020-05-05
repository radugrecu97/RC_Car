def server
def client
def serverName

pipeline {
  // run Docker agent from Dockerfile because sshpass is required
  agent {
    dockerfile {
      dir 'ci/Docker/Dockerfiles/conan'
      args '--network docker_ci_network'
    }
  }

  stages {

      stage('Environment') {
        steps {
          script {
            sh 'printenv'
            sh 'pwd'
            load "${WORKSPACE}/ci/variables.groovy"
            server = Artifactory.server "${env.ARTIFACTORY_NAME}"
            // userHome param is passed in order to have a stable path because otherwise, each  new client will generate
            // a folder in the default home directory under a random string
            client = Artifactory.newConanClient(userHome: "${WORKSPACE}/conan_home".toString())
            serverName = client.remote.add server: server, repo: "${env.ARTIFACTORY_REPO}".toString()
          }
        }
      }


      stage('Build') {
        steps {
          script {
            String command = "create . ${env.CONAN_USER_CHANNEL} -pr ${env.CONAN_DIR_PROFILE} --build=missing"
            client.run(command: command)
            echo "RESULT: ${currentBuild.result}"
          }
        }
      }

      stage('Google Test') {
        steps {
          script {
            sshPublisher(
              continueOnError: false,
              failOnError: true,
              publishers: [
                sshPublisherDesc(
                  // configName is acquired from Manage Jenkins > Configure System > Publish over SSH
                  configName: "${env.PUB_OVER_SSH_CONF_NAME}",
                  verbose: true,
                  continueOnError: false,
                  failOnError: true,
                  transfers: [
                    // copy binaries
                    sshTransfer(
                      sourceFiles: "conan_home/.conan/data/${env.CONAN_PACKAGE_NAME}/${env.CONAN_PACKAGE_VER}/${env.CONAN_USER_CHANNEL}/package/*/bin/",
                      flatten: true, // removes the directory prefix to file so only the file is copied and not the folders tree to it as well
                      cleanRemote: true, // clean the remote directory below before copying
                      remoteDirectory: "${env.PROJECT_NAME}/bin", // appends to the remote directory specified in the configuration
                    ),
                    // copy shared libraries
                    sshTransfer(
                      sourceFiles: "conan_home/.conan/data/*/*/_/_/package/*/lib/*",
                      flatten: true,
                      cleanRemote: true,
                      remoteDirectory: "${env.PROJECT_NAME}/lib",
                    ),
                    sshTransfer(
                       execCommand: "cd jenkins_slave/workspace/${env.PROJECT_NAME} && pwd" // run command in remote host
                     ),
                    // make binaries executable
                    sshTransfer(
                      execCommand: "chmod u+x bin/*" // run command in remote host
                    ),
                    // change library path for shared libraries
                    sshTransfer(
                      execCommand: "chrpath -r lib bin/*"
                    ),
                    // clean reports folder in remote host
                    sshTransfer(
                      execCommand: "rm -rf reports"
                    ),
                    // run Google Test and save xUnit report
                    sshTransfer(
                      execCommand: "bin/Motor_test --gtest_output=xml:reports/gtestresults.xml"
                    ),
                  ]
                )
              ]
            )
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
            String command = "upload ${env.CONAN_PACKAGE_NAME}/*@${env.CONAN_USER_CHANNEL} --all -r ${serverName} --confirm"
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
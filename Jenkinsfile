

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
            def util = load "${env.WORKSPACE}/ci/variables.groovy"
            def server = Artifactory.server util.env.ARTIFACTORY_NAME
            def client = Artifactory.newConanClient(userHome: "${env.WORKSPACE}/conan_home".toString())
            def serverName = client.remote.add server: server, repo: util.env.ARTIFACTORY_REPO
          }
        }
      }


      stage('Build') {
        steps {
          script {
            sh 'printenv'
            sh 'pwd'
            String command = "create . ${util.env.CONAN_USER_CHANNEL} -pr ${util.env.CONAN_DIR_PROFILE} --build=missing"
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
                  configName: "${util.env.PUB_OVER_SSH_CONF_NAME}",
                  verbose: true,
                  continueOnError: false,
                  failOnError: true,
                  transfers: [
                    // copy binaries
                    sshTransfer(
                      sourceFiles: "conan_home/.conan/data/${util.env.CONAN_PACKAGE_NAME}/${util.env.CONAN_PACKAGE_VER}/${util.env.CONAN_USER_CHANNEL}/package/*/bin/",
                      flatten: true, // removes the directory prefix to file so only the file is copied and not the folders tree to it as well
                      cleanRemote: true, // clean the remote directory below before copying
                      remoteDirectory: "${util.env.PROJECT_NAME}/bin", // appends to the remote directory specified in the configuration
                    ),
                    // copy shared libraries
                    sshTransfer(
                      sourceFiles: "conan_home/.conan/data/*/*/_/_/package/*/lib/*",
                      flatten: true,
                      cleanRemote: true,
                      remoteDirectory: "${util.env.PROJECT_NAME}/lib",
                    ),
                     sshTransfer(
                        execCommand: "pwd" // run command in remote host
                      ),
                    // make binaries executable
                    sshTransfer(
                      execCommand: "chmod u+x /home/jenkins/jenkins_slave/workspace/${util.env.PROJECT_NAME}/bin/*" // run command in remote host
                    ),
                    // change library path for shared libraries
                    sshTransfer(
                      execCommand: "chrpath -r /home/jenkins/jenkins_slave/workspace/${util.env.PROJECT_NAME}/lib /home/jenkins/jenkins_slave/workspace/${util.env.PROJECT_NAME}/bin/*"
                    ),
                    // clean reports folder in remote host
                    sshTransfer(
                      execCommand: "rm -rf /home/jenkins/jenkins_slave/workspace/${util.env.PROJECT_NAME}/reports"
                    ),
                    // run Google Test and save xUnit report
                    sshTransfer(
                      execCommand: "/home/jenkins/jenkins_slave/workspace/${util.env.PROJECT_NAME}/bin/Motor_test --gtest_output=xml:/home/jenkins/jenkins_slave/workspace/${util.env.PROJECT_NAME}/reports/gtestresults.xml"
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
            String command = "upload ${util.env.CONAN_PACKAGE_NAME}/*@${util.env.CONAN_USER_CHANNEL} --all -r ${serverName} --confirm"
            def b = client.run(command: command)
            b.util.env.collect()
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
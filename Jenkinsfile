node{
    try {
        pipeline()
    } catch (e) {
        postFailure(e)
    } finally {
        postAlways()
    }
}

def pipeline(){

    def buildImage = docker.image("conanio/gcc8-armv7hf")
    buildImage.inside("-v /var/jenkins_home/RC_Car/conan/profiles/:/home/conan/profiles/ --network docker_ci_network") {

        stage("Get project"){
            checkout scm
        }

        load "$JENKINS_HOME/workspace/RC_Car/ci/variables.groovy"
        def server = Artifactory.server "${env.ARTIFACTORY_NAME}"
        def client = Artifactory.newConanClient(userHome: "${env.WORKSPACE}/conan_home".toString())
        def serverName = client.remote.add server: server, repo: "${env.ARTIFACTORY_REPO}".toString()

        stage("Get dependencies and create app") {
            //client.run(command: "remote remove conan-center" )
            String command = "create . radugrecu97/experimental -pr ./ci/conan/profiles/rpi_gcc8 --build=missing"
            client.run(command: command)
        }

        stage("Upload packages") {
            String command = "upload RC_Car/*@radugrecu97/experimental --all -r ${serverName} --confirm"
            def b = client.run(command: command)
            b.env.collect()
            b.number = "v0.${BUILD_NUMBER}" // BUILD_NUMBER is a Jenkins environment variable
            server.publishBuildInfo b
        }

//         stage("Build application") {
//             String command = "install . -if build_rpi_release -pr=ci/conan/profiles/rpi_gcc8"
//             client.run(command: command)
//             command = "build . -bf build_rpi_release"
//             client.run(command: command)
// //             command = "imports ."
// //             client.run(command: command)
//         }

        stage('SSH transfer') {
            script {
                sshPublisher(
                    continueOnError: false, failOnError: true,
                    publishers: [
                        sshPublisherDesc(
                            configName: "RPi_Testing",
                            verbose: true,
                            transfers: [
                                sshTransfer(
                                    execCommand: "rm -rf Remote_Projects/RC_Car/test_binaries/"
                                ),
                                sshTransfer(
                                    sourceFiles: "conan_home/.conan/data/RC_Car/0.1/radugrecu97/experimental/package/*/bin/",
                                    flatten: true,
                                    remoteDirectory: "/RC_Car/test_binaries"
                                ),
                                sshTransfer(
                                    execCommand: "chrpath -r Remote_Projects/RC_Car/test_binaries/lib Remote_Projects/RC_Car/test_binaries/*"
                                ),
                                sshTransfer(
                                    sourceFiles: "conan_home/.conan/data/*/*/_/_/package/*/lib/*",
                                    flatten: true,
                                    remoteDirectory: "/RC_Car/test_binaries/lib"
                                ),
                                sshTransfer(
                                    execCommand: "chmod u+x Remote_Projects/RC_Car/test_binaries/*"
                                ),
                                sshTransfer(
                                    execCommand: "Remote_Projects/RC_Car/test_binaries/Motor_test --gtest_output=xml:Remote_Projects/RC_Car/reports/gtestresults.xml"
                                ),
                            ]
                        )
                    ]
                )
            }
        }
    }

//     stage("Test project") {
//         node (label: 'slave-rpi') {
//             sh "bin/Motor_test --gtest_output=xml:gtestresults.xml"
//         }
//     }

    println 'This will run only if successful'
}


def postFailure(e) {
    println "Failed because of $e"
    println 'This will run only if failed'
}

def postAlways() {
    println 'This will always run'
//     sleep(time:15,unit:"SECONDS")
    //cleanWs()
}
//Adjust your artifactory instance name/repository and your source code repository
def artifactory_name = "art-03"
def artifactory_repo = "conan-local"
def repo_url = 'https://github.com/radugrecu97/RC_Car.git'
def repo_branch = 'master'

node {
   env.WORKSPACE = pwd()
   def server
   def client
   String serverName

    stage("Get project"){
        git branch: repo_branch, url: repo_url
    }

    checkout scm
    def buildImage = docker.build("conanio/gcc9-armv7hf","Dockerfiles/conan_gcc9_armv7hf/")
    buildImage.inside {

        stage("Configure Artifactory/Conan"){
            server = Artifactory.server artifactory_name
            echo server.toString()
            client = Artifactory.newConanClient()
            serverName = client.remote.add server: server, repo: "conan-local"
        }

        stage("Get dependencies and publish build info"){
            sh "mkdir -p build"
            dir ('build') {
              def b = client.run(command: "install ..")
              server.publishBuildInfo b
            }
        }
    }

    stage("Build/Test project"){
        dir ('build') {
          sh "cmake ../ && cmake --build ."
        }
    }
}
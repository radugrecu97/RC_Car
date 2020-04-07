//Adjust your artifactory instance name/repository and your source code repository
def artifactory_name = "art-01"
def artifactory_repo = "conan-local"
def repo_url = 'https://github.com/radugrecu97/RC_Car.git'
def repo_branch = 'master'

node {

   def server
   def client
   def serverName

    stage("Get project"){
        git branch: repo_branch, url: repo_url
    }

    checkout scm
    def buildImage = docker.build("mconanio/gcc9-armv7hf")
    buildImage.inside {

        stage("Configure Artifactory/Conan"){
            server = Artifactory.server artifactory_name
            client = Artifactory.newConanClient()
            serverName = client.remote.add server: server, repo: artifactory_repo
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
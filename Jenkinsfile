//Adjust your artifactory instance name/repository and your source code repository
def artifactory_name = "art-01"
def artifactory_repo = "conan-local"
def repo_url = 'https://github.com/radugrecu97/RC_Car.git'
def repo_branch = 'master'

node {
   checkout scm
   env.WORKSPACE = pwd()
   def server
   def client
   def buildInfo
   String serverName

    stage("Get project"){
        git branch: repo_branch, url: repo_url
    }


    def buildImage = docker.image("conanio/gcc6")
    buildImage.inside("--network rt_cont_int") {

        stage("Configure Artifactory/Conan"){
            server = Artifactory.server artifactory_name

             // Create a local build-info instance:
            buildInfo = Artifactory.newBuildInfo()
            buildInfo.name = "Conan-pipeline"
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
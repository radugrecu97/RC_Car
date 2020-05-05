//Adjust your artifactory instance name/repository and your source code repository

// GIT
env.REPO_URL = "https://github.com/radugrecu97/RC_Car.git"
env.REPO_BRANCH = "master"
env.PROJECT_NAME = "RC_Car"

// ARTIFACTORY
env.ARTIFACTORY_NAME = "art-01"
env.ARTIFACTORY_REPO = "conan-local"

// CONAN
env.CONAN_USER_CHANNEL = "radugrecu97/experimental"
env.CONAN_DIR_PROFILE = "ci/conan/profiles/rpi_gcc8"
env.CONAN_PACKAGE_NAME = "RC_Car"
env.CONAN_PACKAGE_VER = "0.1"

// JENKINS
env.PUB_OVER_SSH_CONF_NAME = "RPi_Testing"


env.MAX_BUILDS = 10
env.MAX_DAYS = 7
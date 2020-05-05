//Adjust your artifactory instance name/repository and your source code repository

// GIT
conf.REPO_URL = "https://github.com/radugrecu97/RC_Car.git"
conf.REPO_BRANCH = "master"
conf.PROJECT_NAME = "RC_Car"

// ARTIFACTORY
conf.ARTIFACTORY_NAME = "art-01"
conf.ARTIFACTORY_REPO = "conan-local"

// CONAN
conf.CONAN_USER_CHANNEL = "radugrecu97/experimental"
conf.CONAN_DIR_PROFILE = "ci/conan/profiles/rpi_gcc8"
conf.CONAN_PACKAGE_NAME = "RC_Car"
conf.CONAN_PACKAGE_VER = "0.1"

// JENKINS
conf.PUB_OVER_SSH_CONF_NAME = "RPi_Testing"


conf.MAX_BUILDS = 10
conf.MAX_DAYS = 7
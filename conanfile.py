from conans import ConanFile, CMake

class RC_CarConan(ConanFile):
    name = "RC_Car"
    description = "Remote controlled Raspberry Pi Car"
    version = "0.1"
    license="MIT"
    #build_folder="/home/radugrecu97/CLionProjects/RC_Car/build_debug"
    #package_folder="/home/radugrecu97/CLionProjects/RC_Car/build_debug"
    settings = "os", "compiler", "build_type", "arch"
    requires = "spdlog/1.5.0", "gtest/1.10.0"
    options = {"shared": [True, False]}
    default_options = {"shared": True}
    url = "https://github.com/radugrecu97/RC_Car.git"
    generators = "cmake"

import os
from conans import ConanFile, CMake

class RC_CarConan(ConanFile):
    name = "RC_Car"
    version = "0.1"
    license="MIT"
    description = "Remote controlled Raspberry Pi Car"
    #build_folder="/home/radugrecu97/CLionProjects/RC_Car/build_debug"
    #package_folder="/home/radugrecu97/CLionProjects/RC_Car/build_debug"
    settings = "os", "compiler", "build_type", "arch"
    url = "https://github.com/radugrecu97/RC_Car.git"
    exports_sources = "CMakeLists.txt", "src/*", "tests/*", "LICENSE"
    generators = "cmake"
    default_options = {"spdlog:shared": True, "gtest:shared": True}

    def requirements(self):
        #self.requires("wiringpi/2.46@conan/stable")
        self.requires("spdlog/1.5.0")
        self.requires("gtest/1.10.0")

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        self.copy("*", dst="bin", src="bin")

    def deploy(self):
        dest = os.getenv("CONAN_IMPORT_PATH")
        self.copy("*", dst=dest, src="bin")

    # def imports(self):
    #     dest = os.getenv("CONAN_IMPORT_PATH", "bin")
    #     self.copy("*", dst=dest, src="bin")
    #     self.copy("*.so*", dst=dest, src="lib")

import os
from conans import ConanFile, CMake

class RC_CarConan(ConanFile):
    name = "RC_Car"
    version = "0.1"
    license="MIT"
    description = "Remote controlled Raspberry Pi Car"
    settings = "os", "compiler", "build_type", "arch"
    url = "https://github.com/radugrecu97/RC_Car.git"
    exports_sources = "CMakeLists.txt", "src/*", "tests/*", "LICENSE"
    generators = "cmake"
    default_options = {"*:shared": True}
    # install_folder = "./build_rpi_release"
    # build_folder = "./build_rpi_release"

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
        self.copy("*.so*", dst="bin", src="lib")

    def deploy(self):
        self.copy("*", dst="bin", src="bin")
        self.copy("*.so*", dst="bin", src="lib")

    # def imports(self):
    #     self.copy("*", dst="bin", src="bin")
    #     self.copy("*.so*", dst="bin", src="lib")

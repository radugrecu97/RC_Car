from conans import ConanFile, CMake

class RC_CarConan(ConanFile):
    name = "RC_Car"
    description = "Remote controlled Raspberry Pi Car"
    version = "0.1"
    license="MIT"
    #build_folder="/home/radugrecu97/CLionProjects/RC_Car/build_debug"
    #package_folder="/home/radugrecu97/CLionProjects/RC_Car/build_debug"
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "CMakeLists.txt", "main.cpp", "LICENSE"
    options = {"shared": [True, False]}
    default_options = {"shared": True}
    url = "https://github.com/radugrecu97/RC_Car.git"
    generators = "cmake"


    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        self.copy("rc_car", src="bin", dst="bin")

    def requirements(self):
        #self.requires("wiringpi/2.46@conan/stable")
        self.requires("spdlog/1.5.0")
        self.requires("gtest/1.10.0")

    def deploy(self):
        self.copy("rc_car", src="bin", dst="bin")

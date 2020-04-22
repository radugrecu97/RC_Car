cmake_minimum_required(VERSION 3.16.4)
project(RC_Car CXX)
add_definitions("-std=c++11")


#####------------------------------------------------CONSTANTS-----------------------------------------------------#####

set( DIR_SRC ${PROJECT_SOURCE_DIR}/src)
set( DIR_CI ${PROJECT_SOURCE_DIR}/ci)
set( DIR_DOCK ${DIR_CI}/Dockerfiles)
set( DIR_CONF ${DIR_CI}/configurations)

#####-------------------------------------------------CONAN--------------------------------------------------------#####

# Download automatically, you can also just copy the conan.cmake file
if(NOT EXISTS "${CMAKE_BINARY_DIR}/conan.cmake")
    message(STATUS "Downloading conan.cmake from https://github.com/conan-io/cmake-conan")
    file(DOWNLOAD "https://github.com/conan-io/cmake-conan/raw/v0.15/conan.cmake"
            "${CMAKE_BINARY_DIR}/conan.cmake")
endif()

include(${CMAKE_BINARY_DIR}/conan.cmake)

# Install dependencies according to the conanfile. It's also possible to explicitly specify packages.
# The function bellow runs conan_basic_setup as well.
conan_cmake_run(CONANFILE ci/conanfile.txt
                BASIC_SETUP CMAKE_TARGETS
                )


#####------------------------------------------------SUB-DIRS------------------------------------------------------#####


add_subdirectory( tests/Google_tests )
add_executable( RC_Car ${DIR_SRC}/main.cpp )


# The optional parameter is to force the linker to emit RPATH because without it, the executable cannot locate the
# shared libraries. Apparently it's platform issue.
# More info here:
# https://stackoverflow.com/questions/58997230/cmake-project-fails-to-find-shared-library#answer-60126535
# https://github.com/conan-io/conan/issues/2660
target_link_libraries( RC_Car CONAN_PKG::spdlog "-Wl,--disable-new-dtags")



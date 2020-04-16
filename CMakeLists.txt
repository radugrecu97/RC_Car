cmake_minimum_required(VERSION 2.8.12)
project(RC_Car)
add_definitions("-std=c++11")
set(CMAKE_BUILD_TYPE Release)

# Download automatically, you can also just copy the conan.cmake file
if(NOT EXISTS "${CMAKE_BINARY_DIR}/conan.cmake")
    message(STATUS "Downloading conan.cmake from https://github.com/conan-io/cmake-conan")
    file(DOWNLOAD "https://github.com/conan-io/cmake-conan/raw/v0.15/conan.cmake"
            "${CMAKE_BINARY_DIR}/conan.cmake")
endif()

include(${CMAKE_BINARY_DIR}/conan.cmake)

conan_cmake_run(REQUIRES spdlog/1.5.0
                REQUIRES gtest/1.10.0
                BASIC_SETUP
                BUILD missing)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)

add_executable(RC_Car main.cpp)
target_link_libraries(RC_Car ${CONAN_LIBS})
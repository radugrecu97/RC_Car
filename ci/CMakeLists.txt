cmake_minimum_required(VERSION 2.8.12)
project(RC_Car)
add_definitions("-std=c++11")
set(CMAKE_BUILD_TYPE Release)

#####--------------------------------------------CONSTANTS_START---------------------------------------------------#####

set( DIR_ROOT ./..)
set( DIR_SRC ${DIR_ROOT}/src)
set( DIR_LIB ${DIR_ROOT}/external/lib)
set( DIR_HEAD ${DIR_ROOT}/external/include)
set( DIR_CI ./)
set( DIR_DOCK ${DIR_CI}/Dockerfiles)
set( DIR_CONF  ${DIR_CI}/configurations)

#####---------------------------------------------CONSTANTS_END----------------------------------------------------#####





#####---------------------------------------------CONAN_START------------------------------------------------------#####

# Download automatically, you can also just copy the conan.cmake file
if(NOT EXISTS "${CMAKE_BINARY_DIR}/conan.cmake")
    message(STATUS "Downloading conan.cmake from https://github.com/conan-io/cmake-conan")
    file(DOWNLOAD "https://github.com/conan-io/cmake-conan/raw/v0.15/conan.cmake"
            "${CMAKE_BINARY_DIR}/conan.cmake")
endif()

include(${CMAKE_BINARY_DIR}/conan.cmake)

conan_cmake_run(CONANFILE conanfile.txt
                BASIC_SETUP CMAKE_TARGETS
                BUILD missing)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)

# The setup function sets all compiler flags. It is required for the spdlog library as it comes with an external fmt lib
conan_basic_setup()

#####-----------------------------------------------CONAN_END------------------------------------------------------#####





#####---------------------------------------------LIBRARIES_START--------------------------------------------------#####

set( GTEST libgtest.so)
set( SPDLOG libspdlog.so)
link_directories( ${DIR_LIB}/spdlog ${DIR_LIB}/gtest)
include_directories( ${DIR_HEAD} )

#####----------------------------------------------LIBRARIES_END---------------------------------------------------#####



add_executable(RC_Car ${DIR_SRC}/main.cpp)
target_link_libraries(RC_Car ${GTEST} ${SPDLOG} )
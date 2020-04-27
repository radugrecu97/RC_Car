project( Motor_test )

add_executable(Motor_test motor_tests.cpp)

# The optional parameter is to force the linker to emit RPATH because without it, the executable cannot locate the
# shared libraries. Apparently it's platform issue.
# More info here:
# https://stackoverflow.com/questions/58997230/cmake-project-fails-to-find-shared-library#answer-60126535
# https://github.com/conan-io/conan/issues/2660
target_link_libraries( Motor_test CONAN_PKG::gtest "-Wl,--disable-new-dtags")

cmake_minimum_required(VERSION 3.15)
project(unit_testing Fortran)
enable_language(Fortran)

# Required for finding unit test framework
# I suspect Zofu should be a loaded lua module for pck-config variables to
# get loaded into the environment
#find_package(PkgConfig REQUIRED)
#pkg_check_modules(ZOFU REQUIRED zofu>=1.0.0)

# Unit test library
set(ZOFU_DIR "/Users/alexanderbuccheri/Programs/zofu/zofu_library")
find_library(ZOFU REQUIRED "${ZOFU_DIR}/lib")
set(ZOFU_INCLUDE_DIR "${ZOFU_DIR}/include")
include_directories(${ZOFU_INCLUDE_DIR})


# Library
add_library(libunit_testing "")
set_target_properties(libunit_testing
        PROPERTIES
        VERSION 1.0
        SOVERSION 1.0)

target_include_directories(libunit_testing
        PUBLIC
        src/
        )

target_sources(libunit_testing
        PRIVATE
        src/constants.f90
        src/maths_utils.f90
        src/geometry.f90
        )

# Has no dependencies
#add_dependencies(libunit_testing)

set_target_properties(libunit_testing PROPERTIES LIBRARY_OUTPUT_NAME unit_testing)


# Executable
add_executable(unit_testing_exe)

set_target_properties(unit_testing_exe
        PROPERTIES
        RUNTIME_OUTPUT_NAME unit_testing)

set_target_properties(unit_testing_exe
        PROPERTIES
        VERSION 1.0)

target_sources(unit_testing_exe
        PRIVATE
        src/main.f90
        )

target_link_libraries(unit_testing_exe
        PRIVATE
        libunit_testing
        )

# Unit tests
add_executable(test_geometry src/geometry_tests.f90)
target_link_libraries (test_geometry ZOFU libunit_testing)
add_test(NAME UNITTEST_test_geometry COMMAND bin/test_geometry)
enable_testing()

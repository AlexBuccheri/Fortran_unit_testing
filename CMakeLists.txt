cmake_minimum_required(VERSION 3.15)
project(unit_testing Fortran)
enable_language(Fortran)

# ------------------------
# Unit Testing Framework
# ------------------------

# Required for finding unit test framework
# I suspect Zofu should be a loaded lua module for pck-config variables to
# get loaded into the environment
#find_package(PkgConfig REQUIRED)
#pkg_check_modules(ZOFU REQUIRED zofu>=1.0.0)

# Unit test library
set(ZOFU_DIR "/Users/alexanderbuccheri/Programs/zofu/zofu_library")
find_library(ZOFU NAME "libzofu" "zofu" REQUIRED HINTS "${ZOFU_DIR}/lib")
message("-- Zofu library location: ${ZOFU}")
set(ZOFU_INCLUDE_DIR "${ZOFU_DIR}/include")
include_directories(${ZOFU_INCLUDE_DIR})
# Program that generates a unit test driver given a set of modules
#set(ZOFU_DRIVER ${ZOFU_DIR}/bin/zofu-driver)
# My Zofu driver
set(ZOFU_DRIVER ${PROJECT_SOURCE_DIR}/utils/make_zofu_driver.py)

# TODO(Alex) Write a FindZofu.cmake
# TODO(Alex) Zofu has CMake, which is great. Use that instead of building with MESON
# TODO(Alex) Ask them to modify the driver generator to parse test routines from multiple modules
# TODO(Alex) Ask Zofu author if he wants to post a link to this repo, demonstrating how Zofu can be used


# -------------------
# Library
# -------------------
# TODO(Alex) rename the library to something like base
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
        src/units_and_constants/precision.f90

        src/maths/maths_utils.f90
        src/maths/maths_functions.f90

        src/geometry/geometry.f90

        src/asserts/asserts.F90
        )

# Set fortran pre-processing variable from CMake -DDEBUG flag
if(DEBUG)
    set_property(TARGET libunit_testing APPEND PROPERTY
            COMPILE_DEFINITIONS "DEBUG")
endif()


# add_dependencies(libunit_testing FORD)  # Apparently does not exist
set_target_properties(libunit_testing PROPERTIES LIBRARY_OUTPUT_NAME unit_testing)

# -------------------
# Executable
# -------------------
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

# TODO(Alex) Separate unit tests, modules, libraries, bin, src in the cmake build folder

# -------------------
# Unit tests
# -------------------
enable_testing()

# Functions for generating unit test executables
include(cmake/unit_test_functions.cmake)

# A list containing all unit test modules within a given subdirectory
list(APPEND maths_unit_tests "maths_functions_tests.f90"   # Unit tests for maths_functions.f90
                             "maths_utils_tests.f90"       # Unit tests for maths_utils.f90
        )

list(APPEND geometry_unit_tests "geometry_tests.f90"       # Unit tests for geometry.f90
        )

# TODO(Alex) Extend to work with MPI
#create_unit_test_executable(MPI_ENABLED SUBDIR "maths" UNIT_TESTS ${maths_unit_tests} )

# Generates a unit test executable using the Zofu unit testing framework
create_unit_test_executable(SUBDIR "maths" UNIT_TESTS ${maths_unit_tests})

create_unit_test_executable(SUBDIR "geometry" UNIT_TESTS ${geometry_unit_tests})

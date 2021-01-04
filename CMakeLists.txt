cmake_minimum_required(VERSION 3.15)
project(unit_testing Fortran)
enable_language(Fortran)

# TODO(Alex) Do I want to be using CMAKE_BINARY_DIR OR PROJECT_BINARY_DIR?
# Set output folders for exe, libs and modules
set(CMAKE_Fortran_BIN_DIRECTORY ${PROJECT_BINARY_DIR}/bin)
set(CMAKE_Fortran_LIB_DIRECTORY ${PROJECT_BINARY_DIR}/lib)
set(CMAKE_Fortran_MODULE_DIRECTORY ${PROJECT_BINARY_DIR}/modules)


# ------------------------
# External libraries
# ------------------------

# Find Python 3
# https://cmake.org/cmake/help/git-stage/module/FindPython3.html
# Should update to python 3.7: https://docs.python.org/3/whatsnew/3.7.html
find_package(Python3 3.6 COMPONENTS Interpreter) # Can't find Development
if(Python3_FOUND)
    message("-- Python 3 interpreter version: " ${Python3_VERSION})
else()
    message("-- Python 3 interpreter not found")
endif()


# Unit Testing Framework
# I suspect Zofu should be a loaded lua module for pck-config variables to
# get loaded into the environment
# find_package(PkgConfig REQUIRED)
# pkg_check_modules(ZOFU REQUIRED zofu>=1.0.0)

# Unit test library
# TODO(Alex) Pass ZOFU_DIR as a CMake argument
set(ZOFU_DIR "/Users/alexanderbuccheri/Programs/zofu/zofu_library")
find_library(ZOFU NAME "libzofu" "zofu" REQUIRED HINTS "${ZOFU_DIR}/lib")
message("-- Zofu library location: ${ZOFU}")
set(ZOFU_INCLUDE_DIR "${ZOFU_DIR}/include")
include_directories(${ZOFU_INCLUDE_DIR})

# Program that generates a unit test driver given a set of modules
#set(ZOFU_DRIVER ${ZOFU_DIR}/bin/zofu-driver)
# My Zofu driver
set(ZOFU_DRIVER ${CMAKE_SOURCE_DIR}/python/zofu/make_zofu_driver.py)

# TODO(Alex) Write a FindZofu.cmake
# TODO(Alex) Zofu has CMake, which is great. Use that instead of building with MESON
# TODO(Alex) Ask them to modify the driver generator to parse test routines from multiple modules
# TODO(Alex) Ask Zofu author if he wants to post a link to this repo, demonstrating how Zofu can be used


# -------------------
# Library
# -------------------

# TODO(Alex) rename the library to something like base
# TODO(Alex) Note, current appear to be building a static library, not shared lib
# hence why I've also set the archive directory
add_library(libunit_testing "")

set_target_properties(libunit_testing
        PROPERTIES
        VERSION 1.0
        SOVERSION 1.0
        )

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
        src/asserts/errors_warnings.f90

        src/parse/read.f90
        src/parse/command_line.f90
        )

# Set fortran pre-processing variable from CMake -DDEBUG flag
if(DEBUG)
    set_property(TARGET libunit_testing APPEND PROPERTY
            COMPILE_DEFINITIONS "DEBUG")
endif()


set_target_properties(libunit_testing
        PROPERTIES
        LIBRARY_OUTPUT_NAME unit_testing
        ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_Fortran_LIB_DIRECTORY}
        LIBRARY_OUTPUT_DIRECTORY ${CMAKE_Fortran_LIB_DIRECTORY})

# -------------------
# Executable
# -------------------
add_executable(unit_testing_exe)
set(EXE_OUTPUT_NAME unit_testing)

set_target_properties(unit_testing_exe
        PROPERTIES
        RUNTIME_OUTPUT_NAME ${EXE_OUTPUT_NAME}
        VERSION 1.0)

# TODO(Alex) Should I add all source as a target, or is there no need having compiled
# all other modules as a lib?
target_sources(unit_testing_exe
        PRIVATE
        src/main.f90
        )

target_link_libraries(unit_testing_exe
        PRIVATE
        libunit_testing
        )

set_target_properties(unit_testing_exe
        PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY ${CMAKE_Fortran_BIN_DIRECTORY})


# --------------------------
# Install
# --------------------------
if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
    set(CMAKE_INSTALL_PREFIX ${default_install_prefix}
            CACHE STRING "Choose the installation directory. Default location is ${default_install_prefix}"
            FORCE)
endif()

# Destination relative to ${CMAKE_INSTALL_PREFIX}
install(TARGETS libunit_testing
        ARCHIVE DESTINATION lib
        LIBRARY DESTINATION lib)

# Destination relative to ${CMAKE_INSTALL_PREFIX}
install(DIRECTORY ${CMAKE_Fortran_MODULE_DIRECTORY}
        DESTINATION include)



# -------------------
# Unit Testing
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
# Arguments are the relative unit test location SUBDIR and a list of UNIT_TESTS
create_unit_test_executable(SUBDIR "maths" UNIT_TESTS ${maths_unit_tests})

create_unit_test_executable(SUBDIR "geometry" UNIT_TESTS ${geometry_unit_tests})


# -------------------
# Application Testing
# -------------------

# Perform application testing with the pytest framework
# Ultimately one could even avoid output to file by calling the code from
# python and passing the result back to python

include(cmake/python.cmake)
if (Python3_FOUND)
    find_python_module(numpy)

    # The pytest framework makes it easy to write small tests, yet scales to support
    # complex functional testing for applications and libraries
    find_python_module(pytest)

    # MessagePack is an efficient binary serialization format. It lets you
    # exchange data among multiple languages like JSON. But it's faster and smaller.
    # This package provides CPython bindings for reading and writing MessagePack data.
    # As such, might be able to use with fortran
    # TODO(Alex) Look at CPython-fortran bindings for this
    find_python_module(msgpack)
endif()


# A set of application tests
# As tests are written, they can be added to the MOLECULE_APP_TESTS list
# or added to a new list

# `co2_distance_matrix` is a test. It should have an input file and python file
# (same name, different extensions), with the latter to perform the asserts.
# These are written in tests/
# In principle, one could write the input in the python file (which would be cleaner)
#set(MOLECULE_APP_TESTS co2_distance_matrix)
#
#foreach(INPUT ${MOLECULE_APP_TESTS})
#
#    # Serial tests for MOLECULE_APP_TESTS
#    add_test(
#            NAME APPLICATIONTEST_SERIAL_${INPUT}
#            COMMAND pytest -s tests/${INPUT}.py --build_type ${CMAKE_BUILD_TYPE} --exe ${EXE_OUTPUT_NAME}
#            WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}/tests
#            # CONFIGURATIONS "" ${FAST_PRIVATE} # If one wishes to set different ctest targets
#    )
#
#    # Can also set useful test properties
#    set_tests_properties(APPLICATIONTEST_SERIAL_${INPUT}
#            PROPERTIES LABELS MOLECULE_SERIAL   # Assign a label when one has multiple methods to test
#            # WILL_FAIL TRUE                    # When one intentionally writes a failing test
#            )
#
#    # MPI + threaded tests
#    # add_test would look the same but one would pass a flag to the python runner:
#    # COMMAND python3 tests/${INPUT}.py -mpi tests/${INPUT}.in
#    # This simply depends on how the test framework is set up
#
#endforeach()


# Can create custom target commands with:
# add_custom_target( ctest_all ctest -C all )
# Use this to split app tests, unit tests, slow tests and fast tests



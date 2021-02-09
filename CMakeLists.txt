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

# https://cmake.org/cmake/help/git-stage/module/FindPython3.html
# Should update to python 3.7: https://docs.python.org/3/whatsnew/3.7.html
find_package(Python3 3.6 COMPONENTS Interpreter) # Can't find Development
if(Python3_FOUND)
    message("-- Python 3 interpreter version: " ${Python3_VERSION})
else()
    message("-- Python 3 interpreter not found")
endif()

# Find Unit Testing Framework
include(cmake/findZofu.cmake)

# Find MPI library
include(cmake/mpi.cmake)

# -------------------
# Library
# -------------------

# TODO(Alex) rename the library to something like base
# TODO(Alex) Note, currently appear to be building a static library, not shared lib
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

# Use assertions if compiled in Debug mode
option("USE_ASSERT" OFF)
if(CMAKE_BUILD_TYPE MATCHES Debug)
    set_property(TARGET libunit_testing APPEND PROPERTY
            COMPILE_DEFINITIONS "USE_ASSERT")
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

# TODO(Alex) Demonstrate an MPI unit test
#create_unit_test_executable(ENABLE_MPI SUBDIR "maths" UNIT_TESTS ${maths_unit_tests} )

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

    find_python_module(scipy)

    # The pytest framework makes it easy to write small tests, yet scales to support
    # complex functional testing for applications and libraries
    find_python_module(pytest)
    find_python_module(unittest)

    # MessagePack is an efficient binary serialization format. It lets you
    # exchange data among multiple languages like JSON. But it's faster and smaller.
    # This package provides CPython bindings for reading and writing MessagePack data.
    # As such, might be able to use with fortran
    # TODO(Alex) Look at CPython-fortran bindings for this
    find_python_module(msgpack)
endif()

# A set of application tests
# New tests can either be added to the MOLECULE_APP_TESTS list or added to a new list

# `co2_distance_matrix` is a test. It should have an input file and python file
# (same name, different extensions), with the latter to perform the asserts.
# In principle, one could write the input in the python file (which would be cleaner)

set(MOLECULE_APP_TESTS co2_distance_matrix)

foreach(INPUT ${MOLECULE_APP_TESTS})
    # Serial tests for MOLECULE_APP_TESTS
    # These are written and ran in tests/
    add_test(
            NAME APPLICATIONTEST_SERIAL_${INPUT}
            COMMAND pytest -s ${INPUT}.py --build_type "serial" ${CMAKE_BUILD_TYPE} --exe ${EXE_OUTPUT_NAME}
            WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}/tests
            # CONFIGURATIONS "" ${FAST_PRIVATE} # If one wishes to set different ctest targets
    )
    # Can also set useful test properties
    set_tests_properties(APPLICATIONTEST_SERIAL_${INPUT}
            PROPERTIES LABELS MOLECULE_SERIAL   # Assign a label for extra ctest timing info
            WILL_FAIL FALSE                     # If TRUE, allows one intentionally write a failing test OR flag issues
            )
endforeach()


# MPI + threaded tests
# add_test would look the same but with different flags
# Defaults are set for threads and cores, however they can also be specified
# COMMAND pytest -s ${INPUT}.py --build_type "hybrid" ${CMAKE_BUILD_TYPE} --exe ${EXE_OUTPUT_NAME}

# TODO(Alex)
# Can create custom target commands with:
# add_custom_target( ctest_all ctest -C all )
# Use this to split app tests, unit tests, slow tests and fast tests



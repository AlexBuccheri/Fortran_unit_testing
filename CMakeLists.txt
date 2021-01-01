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
# TODO(Alex) Ask them to modify the driver generator to parse test routines from
# multiple modules
# TODO(Alex) Ask Zofu author if he wants to post a link to this repo, demonstrating
# how Zofu can be used



# -------------------
# External libraries
# -------------------

option(ENABLE_DOCS "Enable documentation" OFF)

# TODO(Alex) Make these functions
# TODO(Alex) Use LOWER and compare to lowercase strings

# https://github.com/Fortran-FOSS-Programmers/ford/wiki/Writing-Documentation
if (${ENABLE_DOCS} STREQUAL "FORD")
# https://github.com/Fortran-FOSS-Programmers/ford/wiki
# Some examples. JSON library (it's a mess): https://github.com/jacobwilliams/json-fortran/blob/master/CMakeLists.txt
# https://github.com/hornekyle/CommonModules/blob/master/CMakeLists.txt    THIS IS THE ONE TO FOLLOW

    message(STATUS "Build FORD Documentation")
#    set(doc_dir documentation)
#    set ( DOC_DIR "${PROJECT_BINARY_DIR}/doc" )
#    set ( PAGES_DIR "${PROJECT_SOURCE_DIR}/pages" )
#    set ( PROJ_DIR "${PROJECT_SOURCE_DIR}/src" )
#    set ( FORD_PROJECT_FILE "${PROJECT_SOURCE_DIR}/json-fortran.md" )


    #find_package(Ford REQUIRED)
    # TODO(Alex) Difference between find_package and find_program
    find_program (FORD ford REQUIRED)
endif()

if (${ENABLE_DOCS} STREQUAL "doxygen")
    message(STATUS "Build doxygen Documentation")
    set(doc_dir documentation)
    find_package(Doxygen REQUIRED)
endif()

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

# TODO(Alex) Move this function
# TODO(Alex) When this function gets moved, look into how to pass ${ZOFU_DRIVER},
# and the libraries: ${ZOFU} and libunit_testing, to it

function(create_unit_test_executable)
    # Set up a unit test executable with the name `test_SUBDIR`
    # This function assumes the fortran ZOFU unit test framework, although this
    # can easily be modified by changing the add_custom_command arguments

    # Define the CMake function signature keywords and their types
    # Of the general form: set(type KEYWORD)
    set(options)                                    # Binary options (none for this function)
    set(oneValueArgs SUBDIR)                        # Single-value options
    set(multiValueArgs UNIT_TESTS)                  # Multi-value options: Multiple arguments or list/s
    # TODO(Alex) Use a better prefix
    cmake_parse_arguments(MY_FUNC                   # Prefix for all function arguments within function body
                          "${options}"              # Assign the binary options for the function
                          "${oneValueArgs}"         # Assign the single-value options for the function
                          "${multiValueArgs}"       # Assign the multi-value options for the function
                          ${ARGV})                  # ${ARGN} or ${ARGV}. (I think) ${ARGV} means accept a variable
                                                    # number of arguments, which one want for a list of no fixed size

    list(TRANSFORM MY_FUNC_UNIT_TESTS PREPEND "${PROJECT_SOURCE_DIR}/src/${MY_FUNC_SUBDIR}/")

    # Runs the unix command specified by COMMAND
    # Create a unit test driver that runs all tests in the respective subdirectory
    add_custom_command(
            OUTPUT ${PROJECT_BINARY_DIR}/${MY_FUNC_SUBDIR}_driver.f90
            COMMAND ${ZOFU_DRIVER} ${MY_FUNC_UNIT_TESTS} ${PROJECT_BINARY_DIR}/${MY_FUNC_SUBDIR}_driver.f90
            COMMENT "Generating ${PROJECT_BINARY_DIR}/${MY_FUNC_SUBDIR}_driver.f90")

    # Create the test driver executable and add module targets:
    # all unit test modules and the test driver
    add_executable(test_${MY_FUNC_SUBDIR})

    target_sources(test_${MY_FUNC_SUBDIR}
             PRIVATE
             ${MY_FUNC_UNIT_TESTS}
             ${PROJECT_BINARY_DIR}/${MY_FUNC_SUBDIR}_driver.f90
            )
    # Ensure our library gets compiled if one attempts to build the unit test executable
    add_dependencies(test_${MY_FUNC_SUBDIR} libunit_testing)

    # Link the libraries that the unit test executable will dependent on
    # We assume that ZOFU is built and found by CMake at this point
    target_link_libraries(test_${MY_FUNC_SUBDIR} ${ZOFU} libunit_testing)

endfunction()


# A list containing all unit test modules within a given subdirectory
# The naming convention for a unit test of the source `module_name.f90` is
# `module_name_tests.f90`, although one is not required to use this
list(APPEND maths_unit_tests "maths_functions_tests.f90"
                             "maths_utils_tests.f90")

list(APPEND geometry_unit_tests "geometry_tests.f90")

create_unit_test_executable(SUBDIR "maths" UNIT_TESTS ${maths_unit_tests})

create_unit_test_executable(SUBDIR "geometry" UNIT_TESTS ${geometry_unit_tests})


#add_subdirectory(src/geometry)
#add_subdirectory(src/maths)











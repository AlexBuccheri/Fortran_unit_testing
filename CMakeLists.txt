cmake_minimum_required(VERSION 3.15)
project(unit_testing Fortran)
enable_language(Fortran)

# Required for finding unit test framework
# I suspect Zofu should be a loaded lua module for pck-config variables to
# get loaded into the environment
#find_package(PkgConfig REQUIRED)
#pkg_check_modules(ZOFU REQUIRED zofu>=1.0.0)


# TODO(Alex) Write a FindZofu.cmake
# Unit test library
set(ZOFU_DIR "/Users/alexanderbuccheri/Programs/zofu/zofu_library")
find_library(ZOFU NAME "libzofu" "zofu" REQUIRED HINTS "${ZOFU_DIR}/lib")
message("-- Zofu library location: ${ZOFU}")
set(ZOFU_INCLUDE_DIR "${ZOFU_DIR}/include")
include_directories(${ZOFU_INCLUDE_DIR})



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

# -------------------
# Unit tests
# -------------------
#enable_testing()

# Geometry
## https://stackoverflow.com/questions/2937128/cmake-add-custom-command-not-being-run
#TODO(Alex) Add a second test module in this directory and link to the same driver
add_custom_command(
        OUTPUT ${PROJECT_BINARY_DIR}/geometry_tests_driver.f90
        COMMAND ${ZOFU_DIR}/bin/zofu-driver ${PROJECT_SOURCE_DIR}/src/geometry/geometry_tests.f90
                ${PROJECT_BINARY_DIR}/geometry_tests_driver.f90
        DEPENDS ${PROJECT_SOURCE_DIR}/src/geometry/geometry_tests.f90
        COMMENT "Generating ${PROJECT_BINARY_DIR}/geometry_tests_driver.f90"
)

add_executable(test_geometry)

target_sources(test_geometry
        PRIVATE
        src/geometry/geometry_tests.f90
        ${PROJECT_BINARY_DIR}/geometry_tests_driver.f90
        )

add_dependencies(test_geometry libunit_testing)
target_link_libraries(test_geometry ${ZOFU} libunit_testing)
add_test(NAME UNITTEST_test_geometry COMMAND bin/test_geometry)

# maths
add_custom_command(
        OUTPUT ${PROJECT_BINARY_DIR}/maths_utils_tests_driver.f90
        COMMAND ${ZOFU_DIR}/bin/zofu-driver ${PROJECT_SOURCE_DIR}/src/maths/maths_utils_tests.f90
        ${PROJECT_BINARY_DIR}/maths_utils_tests_driver.f90
        DEPENDS ${PROJECT_SOURCE_DIR}/src/maths/maths_utils_tests.f90
        COMMENT "Generating ${PROJECT_BINARY_DIR}/maths_utils_tests_driver.f90")

add_executable(test_maths_utils)

target_sources(test_maths_utils
        PRIVATE
        src/maths/maths_utils_tests.f90
        ${PROJECT_BINARY_DIR}/maths_utils_tests_driver.f90
        )

add_dependencies(test_maths_utils libunit_testing)
target_link_libraries(test_maths_utils ${ZOFU} libunit_testing)
add_test(NAME UNITTEST_test_maths_utils COMMAND bin/test_maths_utils)

# Test all
# TODO(Alex) Write a python script that runs each test exe, parses the results
# and gives a full summary ?
# CI can just run each separately

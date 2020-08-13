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
find_library(ZOFU NAME "libzofu" "zofu" REQUIRED HINTS "${ZOFU_DIR}/lib")
message("-- Zofu library location: ${ZOFU}")
set(ZOFU_INCLUDE_DIR "${ZOFU_DIR}/include")
include_directories(${ZOFU_INCLUDE_DIR})

# -------------------
# Library
# -------------------
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
# add_dependencies(libunit_testing)

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
## https://stackoverflow.com/questions/2937128/cmake-add-custom-command-not-being-run

add_custom_command(
        OUTPUT ${PROJECT_BINARY_DIR}/geometry_tests_driver.f90
        COMMAND ${ZOFU_DIR}/bin/zofu-driver ${PROJECT_SOURCE_DIR}/src/geometry_tests.f90 ${PROJECT_BINARY_DIR}/geometry_tests_driver.f90
        DEPENDS src/geometry_tests.f90
        COMMENT "Generating ${PROJECT_BINARY_DIR}/geometry_tests_driver.f90"
)

add_executable(test_geometry)

target_sources(test_geometry
        PRIVATE
        src/geometry_tests.f90
        ${PROJECT_BINARY_DIR}/geometry_tests_driver.f90
        )

add_dependencies(test_geometry libunit_testing)
target_link_libraries(test_geometry ${ZOFU} libunit_testing)
add_test(NAME UNITTEST_test_geometry COMMAND bin/test_geometry)




# FindZofu
# --------
#
# Find the Zofu includes and library.
# Zofu is a requirement, therefore CMake will fail if it's not found.
#
# This module defines the following variables:
#
#   ZOFU                  - Zofu library.
#   ZOFU_INCLUDE_DIR      - Location of Zofu include files (modules).
#   ZOFU_DRIVER           - Python script to parse test modules and create a
#                           test driver program.
#
# TODO(Alex) Add ExternalProject_add such that CMake can pull and build if not found
# TODO(Alex) Configure so PkgConfig works
# find_package(PkgConfig REQUIRED)
# pkg_check_modules(ZOFU REQUIRED zofu>=1.0.0)

# Initialised as an empty string
set(ZOFU_PATH "" CACHE STRING "Location of external Zofu unit-testing library")

find_library(ZOFU NAME "libzofu" "zofu" REQUIRED HINTS "${ZOFU_PATH}/lib")
message("-- Zofu library location: ${ZOFU}")
set(ZOFU_INCLUDE_DIR "${ZOFU_PATH}/include")
include_directories(${ZOFU_INCLUDE_DIR})

# TODO(Alex) Open issue to extend the driver generator to parse test routines from multiple modules
# Program that generates a unit test driver given a test module.
# Unfortunately this does not take multiple modules as arguments
#set(ZOFU_DRIVER ${ZOFU_DIR}/bin/zofu-driver)

# My Zofu driver, which accepts multiple modules as arguments,
# reducing the number of unit test driver .f90 programs
set(ZOFU_DRIVER ${CMAKE_SOURCE_DIR}/python/zofu/make_zofu_driver.py)

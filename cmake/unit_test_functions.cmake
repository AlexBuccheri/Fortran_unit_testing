# TODO(Alex) Pass ${ZOFU_DRIVER}, and the libraries: ${ZOFU} and libunit_testing, to the function
# It appears that functions have access to variables set in the main CMakeLists.txt
# Need to investigate scope in CMake in more detail

function(create_unit_test_executable)
    # Create a unit test executable with the name `test_SUBDIR`
    # This function assumes the fortran ZOFU unit test framework, although this
    # can easily be modified by changing the add_custom_command arguments

    # https://cmake.org/cmake/help/latest/command/cmake_parse_arguments.html
    # Define the CMake function signature keywords and their types
    # Of the general form: set(type KEYWORD)
    set(options MPI_ENABLED)                        # Binary options
    set(oneValueArgs SUBDIR)                        # Single-value options
    set(multiValueArgs UNIT_TESTS)                  # Multi-value options: Multiple arguments or list/s
    # TODO(Alex) Use a better prefix
    cmake_parse_arguments(MY_FUNC                   # Prefix for all function arguments within function body
            "${options}"                            # Assign the binary options for the function
            "${oneValueArgs}"                       # Assign the single-value options for the function
            "${multiValueArgs}"                     # Assign the multi-value options for the function
            ${ARGV})                                # ${ARGN} or ${ARGV}. (I think) ${ARGV} means accept a variable
                                                    # number of arguments, which one want for a list of no fixed size

    # Full file path
    list(TRANSFORM MY_FUNC_UNIT_TESTS PREPEND "${PROJECT_SOURCE_DIR}/src/${MY_FUNC_SUBDIR}/")

    # Runs the unix command specified by COMMAND:
    # Create a unit test driver that runs all tests in the respective subdirectory
    # using ${ZOFU_DRIVER} (which must be my custom script, not the binary supplied with the library)
    IF(NOT ${MY_FUNC_MPI_ENABLED})
    add_custom_command(
            OUTPUT ${PROJECT_BINARY_DIR}/${MY_FUNC_SUBDIR}_driver.f90
            COMMAND ${ZOFU_DRIVER} ${MY_FUNC_UNIT_TESTS} ${PROJECT_BINARY_DIR}/${MY_FUNC_SUBDIR}_driver.f90
            COMMENT "Generating ${PROJECT_BINARY_DIR}/${MY_FUNC_SUBDIR}_driver.f90")
    ELSE()
        # TODO(Alex) Extend to work with MPI
        message(FATAL_ERROR "Custom Zofu driver has not yet been extended to work with MPI" )
    ENDIF()

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
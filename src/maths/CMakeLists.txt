# Set up unit test executable (only)

# List containing all unit test modules within this subdirectory
# Naming convention for a unit test of `module_name.f90` is `module_name_tests.f90`
list(APPEND maths_unit_tests "maths_functions_tests.f90"
                             "maths_utils_tests.f90")

list(TRANSFORM maths_unit_tests PREPEND "${PROJECT_SOURCE_DIR}/src/maths/")

# Create a unit test driver that runs all tests in the respective subdirectory
add_custom_command(
        OUTPUT ${PROJECT_BINARY_DIR}/maths_driver.f90
        COMMAND ${ZOFU_DRIVER} ${maths_unit_tests} ${PROJECT_BINARY_DIR}/maths_driver.f90
        COMMENT "Generating ${PROJECT_BINARY_DIR}/maths_driver.f90")

# Create the test driver executable and add module targets:
# i.e all unit test modules and the test driver
add_executable(test_maths)

target_sources(test_maths
        PRIVATE
        ${maths_unit_tests}
        ${PROJECT_BINARY_DIR}/maths_driver.f90
        )

# Ensure our library is compiled if one attempts to build the unit test executable
add_dependencies(test_maths libunit_testing)

# Link the libraries that the unit test executable will dependent on
target_link_libraries(test_maths ${ZOFU} libunit_testing)
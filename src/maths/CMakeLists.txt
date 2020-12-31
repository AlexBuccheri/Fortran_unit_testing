

# Unit tests

#add_custom_command(
#        OUTPUT ${PROJECT_BINARY_DIR}/maths_utils_tests_driver.f90
#        COMMAND ${ZOFU_DIR}/bin/zofu-driver ${PROJECT_SOURCE_DIR}/src/maths/maths_utils_tests.f90
#        ${PROJECT_BINARY_DIR}/maths_utils_tests_driver.f90
#        DEPENDS ${PROJECT_SOURCE_DIR}/src/maths/maths_utils_tests.f90
#        COMMENT "Generating ${PROJECT_BINARY_DIR}/maths_utils_tests_driver.f90")
#
#add_executable(test_maths_utils)
#
#target_sources(test_maths_utils
#        PRIVATE
#        src/maths/maths_utils_tests.f90
#        ${PROJECT_BINARY_DIR}/maths_utils_tests_driver.f90
#        )
#
#add_dependencies(test_maths_utils libunit_testing)
#target_link_libraries(test_maths_utils ${ZOFU} libunit_testing)

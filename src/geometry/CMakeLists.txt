# Geometry
## https://stackoverflow.com/questions/2937128/cmake-add-custom-command-not-being-run
#TODO(Alex) Add a second test module in this directory and link to the same driver
#add_custom_command(
#        OUTPUT ${PROJECT_BINARY_DIR}/geometry_tests_driver.f90
#        COMMAND ${ZOFU_DIR}/bin/zofu-driver ${PROJECT_SOURCE_DIR}/src/geometry/geometry_tests.f90
#        ${PROJECT_BINARY_DIR}/geometry_tests_driver.f90
#        DEPENDS ${PROJECT_SOURCE_DIR}/src/geometry/geometry_tests.f90
#        COMMENT "Generating ${PROJECT_BINARY_DIR}/geometry_tests_driver.f90"
#)
#
#add_executable(test_geometry)
#
#target_sources(test_geometry
#        PRIVATE
#        src/geometry/geometry_tests.f90
#        ${PROJECT_BINARY_DIR}/geometry_tests_driver.f90
#        )
#
#add_dependencies(test_geometry libunit_testing)
#target_link_libraries(test_geometry ${ZOFU} libunit_testing)
#add_test(NAME UNITTEST_test_geometry COMMAND bin/test_geometry)
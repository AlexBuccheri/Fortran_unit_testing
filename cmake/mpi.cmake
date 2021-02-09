# If not provided as a build argument, default to off
option(ENABLE_MPI "Build with MPI enabled" OFF)

if(ENABLE_MPI)
    find_package(MPI REQUIRED)
    include_directories(${MPI_Fortran_INCLUDE_PATH})
    message(STATUS "MPI_Fortran_INCLUDE_PATH ${MPI_Fortran_INCLUDE_PATH}")

    set(LIBS ${LIBS} ${MPI_Fortran_LINK_FLAGS} ${MPI_Fortran_LIBRARIES})
    string(REGEX REPLACE "^ " "" LIBS "${LIBS}")
    message(STATUS "Build with MPI support")
else()
    message(STATUS "Build without MPI support")
endif()
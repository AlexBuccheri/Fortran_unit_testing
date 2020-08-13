# Unit Testing Frameworks for Fortran
Example unit tests for several popular unit testing frameworks
available for Fortran 95 and above. 

This project will include a CMake build file demonstrating installation and linking for each.

## Unit Test Frameworks Currently Included
* [Zofu](https://github.com/acroucher/zofu)

## Unit Test Frameworks to Include
* Fruit
* PFUnit 

## Writing Unit Tests and Adding to CMake

Each source subdirectory should have one test per module, with the naming convention *module_tests.f90* and a driver 
that calls all of the tests. The driver is generated when building with CMake. Specifically, *add_custom_command* calls 
the driver supplied by th zofu library. 

A test executable is buildable for each subdirectory.

Would also like a test_all but I'm still considering ways of implementing. 

## To Dos
* Move zofu unit test into its own source directory OR rename 
* Write FindZofu.cmake 
* Include in that, a script that pulls Zofu off of github and builds it in a user-
specified location => can supply that via a cmake function 

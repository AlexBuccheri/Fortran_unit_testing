# Unit Testing Frameworks for Fortran
Example unit tests for several popular unit testing frameworks
available for Fortran 95 and above. 

This project will include a CMake build file demonstrating installation and linking for each.

## Unit Test Frameworks Currently Included
* [Zofu](https://github.com/acroucher/zofu)

## Unit Test Frameworks to Include
* [Natural Fruit](https://github.com/cibinjoseph/naturalFRUIT)
* [PFUnit](https://github.com/Goddard-Fortran-Ecosystem/pFUnit)

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

## Documentation 
Documentation written with FORD:
https://github.com/Fortran-FOSS-Programmers/ford/wiki/Writing-Documentation

## External Libraries/Dependencies 
Potential means of keeping track of external dependencies:
* git submodules
* Cmake `ExternalProject` Command
* [vkpkg](https://docs.microsoft.com/en-us/cpp/build/vcpkg?view=msvc-160) although fortran support appears limited
* [Fortran Package Manager](https://github.com/fortran-lang/fpm)  
* Custom BASH or python script that pulls the relevant packages from github and builds 

### Git Submodules
Submodule information is stored in `$ROOT/.gitmodules`, `$ROOT/.git/config` and `$ROOT/.git/modules`.

Git submodules can be added to the external folder using the command:   
`cd external && git submodule add -b master [URL to Git repo]`
which will track the master branch of the project.

An issue with git submodules is that it is not a package manager, so if the external libraries also have external dependencies
then one will have to download and install those separately.  

Useful references on submodules:
* https://www.vogella.com/tutorials/GitSubmodules/article.html
* https://github.blog/2016-02-01-working-with-submodules/
* https://www.atlassian.com/git/tutorials/git-submodule

### Fortran Package Manager

#TODO(Alex) Add Cmake commands to build external dependencies? 
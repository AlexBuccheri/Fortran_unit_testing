#!/usr/bin/python3

"""
 Python Zofu Test Driver Generator

 Zofu unit test framework for fortran has its own binary to generate
 a test driver .f90 file from a unit testing module.
 Unfortunately, this binary is only able to create a single driver.f90 per
 test module.

 This script will generate a test driver given an arbitrary number of test
 modules.

 The Zofu unit testing framework for fortran is available here:
 https://github.com/acroucher/zofu
"""

__author__ = "Alexander Buccheri"
__copyright__ = "Copyright 2021"
__license__ = "GPL"
__email__ = "abuccheri@physik.hu-berlin.de"

import sys

def parse_fortran_module(file_name: str) -> tuple:
    """
    Given a fortran file, extract the module name,
    any subroutines beginning with test_ (indicating a unit test)
    and the first line below each subroutine name (if a comment)
    :param file_name: file name
    :return: module_name, subroutine = list of dicts,
        {'name':'test_name', 'comment':'test comment'}
    """

    fid = open(file_name, 'r')
    # TODO(Alex) Check file exists
    lines = fid.readlines()
    fid.close()

    module_name = None
    subroutines = []

    for i, line in enumerate(lines):
        line_parts = line.lower().split()

        if len(line_parts) == 0:
            # Skip blank lines
           continue

        if line_parts[0] == 'module':
            module_name = line_parts[1]

        routine_is_unit_test = line_parts[0] == 'subroutine' and line_parts[1][0:5] == 'test_'

        if routine_is_unit_test:
            first_bracket = line_parts[1].index('(')
            routine_name = line_parts[1][:first_bracket]
            next_line = lines[i+1]

            if next_line.split()[0] == '!':
                # Use test comment
                comment_start = next_line.index('!')
                test_comment = next_line[comment_start + 1:].rstrip()
            else:
                test_comment = routine_name

            subroutines.append({'name': routine_name,
                                'comment': test_comment})

    # TODO(Alex) Would really like to say which one
    assert module_name is not None, "One or more.f90 files do not contain a module"

    return module_name, subroutines


def parse_fortran_source(fortran_source: list):
    """
    Given a list of fortran .f90 files extract the module names
    and unit test subroutine names.

    :param fortran_source: List of file names
    :return: tuple: list of module names, list of subroutine dictionaries
    """

    modules = []
    subroutines = []

    for file in fortran_source:
        module_name, test_subroutines = parse_fortran_module(file)
        modules.append(module_name)
        subroutines.extend(test_subroutines)

    return modules, subroutines


def generate_zofu_driver(driver_name: str, modules: list, subroutines: list) -> str:
    """
    Generate the Zofu test driver program
    #TODO(Alex) Make sure this works for MPI too => Change use zofu and stop statements
    :param driver_name: string, driver name
    :param modules: list of module names
    :param subroutines: list of dictionaries. Each dictionary should contain keys = ['name', 'comment']
    :return: Zofu test driver string
    """
    indent = ' '*3
    extensions = ['.f90', '.f95', '.f03', '.f08']

    if driver_name[-4].lower in extensions:
        driver_name = driver_name[:-4]

    driver_string = 'program ' + driver_name + '\n'
    driver_string += indent + 'use zofu \n'

    for module in modules:
        driver_string += indent + 'use ' + module + '\n'

    driver_string += indent + 'implicit none \n'
    driver_string += indent + 'type(unit_test_type) :: test \n\n'
    driver_string += indent + 'call test%init() \n\n'

    for subroutine in subroutines:
        driver_string += indent + 'call test%run(' + subroutine['name'] + ', "' \
                         + subroutine['comment'] + '") \n\n'

    driver_string += indent + 'call test%summary() \n\n'
    driver_string += indent + 'if (test%failed) stop 1 \n\n'
    driver_string += 'end program ' + driver_name

    return driver_string


def main():
    """
    Parse fortran unit test modules and return a test driver
    that calls each subroutine prefixed with 'test_'.
    See description of script for more details. Call with:

    python3 make_zofu_driver.py module1.f90 module2.F90 test_driver.f90
    """
    assert len(sys.argv), \
        'Must provide at least one module and the test driver name as script args'
    fortran_source = sys.argv[1:-1]
    driver_name = sys.argv[-1]

    modules, subroutines = parse_fortran_source(fortran_source)
    driver_string = generate_zofu_driver(driver_name, modules, subroutines)

    fid = open(driver_name)
    fid.write(driver_string)
    fid.close()
    return


main()

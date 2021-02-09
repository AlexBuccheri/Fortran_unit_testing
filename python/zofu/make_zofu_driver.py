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
import argparse
import os.path

def parse_fortran_module(file_name: str) -> tuple:
    """
    Given a fortran file, extract the module name,
    any subroutines beginning with test_ (indicating a unit test)
    and the first line below each subroutine name (if a comment)

    :param file_name: file name
    :return: module_name, subroutine = list of dicts,
        {'name':'test_name', 'comment':'test comment'}
    """

    if not os.path.isfile(file_name):
        print("File: %s does not exist" % file_name)
        sys.exit()

    fid = open(file_name, 'r')
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

    # TODO(Alex) Would really like to say which one - check out numpy's assert
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


def generate_zofu_driver(driver_name: str, modules: list, subroutines: list, use_mpi: bool) -> str:
    """
    Generate the Zofu test driver program

    :param driver_name: string, driver name
    :param modules: list of module names
    :param subroutines: list of dictionaries. Each dictionary should contain keys = ['name', 'comment']
    :param use_mpi: bool, Unit tests are serial or MPI
    :return: Zofu test driver string
    """
    indent = ' '*3

    # Specific to .find
    not_found = -1
    assert driver_name.find('/') == not_found, "driver name should not include '/'"

    # Remove any trailing extensions
    extensions = ['.f90', '.f95', '.f03', '.f08']
    if driver_name[-4:].lower() in extensions:
        driver_name = driver_name[:-4]

    zofu_module = 'use zofu_mpi \n' if use_mpi else 'use zofu \n'
    zofu_type = 'unit_test_mpi_type' if use_mpi else 'unit_test_type'

    driver_string = 'program ' + driver_name + '\n'
    driver_string += indent + zofu_module

    for module in modules:
        driver_string += indent + 'use ' + module + '\n'

    driver_string += indent + 'implicit none \n'
    driver_string += indent + 'type(' + zofu_type + ') :: test \n\n'
    driver_string += indent + 'call test%init() \n\n'

    for subroutine in subroutines:
        driver_string += indent + 'call test%run(' + subroutine['name'] + ', "' \
                         + subroutine['comment'] + '") \n\n'

    driver_string += indent + 'call test%summary() \n\n'
    # TODO(Alex) Consider stopping with mpi_abort if MPI
    driver_string += indent + 'if (test%failed) stop 1 \n\n'
    driver_string += 'end program ' + driver_name

    return driver_string


def parse_cmd_line_args() -> tuple:
    """
    Parse command-line options
    :return: command-line options: mpi (logical), modules (list), driver (str)
    """

    description =  \
        "Usage: python3 -mpi -mod make_zofu_driver.py module1.f90 module2.F90 ... -driver test_driver.f90"

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-mpi',
                        help='Indicate that the tests are MPI-based. '
                             'If the option is excluded, the default is serial',
                        dest='use_mpi',
                        default=False,
                        action='store_true')

    parser.add_argument('-mod',
                        dest='module_files',
                        help="Module files containing unit tests.",
                        type=str,
                        nargs='+')

    parser.add_argument('-driver',
                        dest='full_path_driver_name',
                        help="Name for the test driver that runs the unit "
                             "tests defined in the specified modules.",
                        type=str,
                        default='test_driver.f90')

    args = parser.parse_args()
    assert len(args.module_files) > 0, \
        "Requires at least one command-line argument for a test module"

    return args.use_mpi, args.module_files, args.full_path_driver_name


def main():
    """
    Parse fortran unit test modules and return a test driver
    that calls each subroutine prefixed with 'test_'.
    See description of script for more details.
    """
    use_mpi, fortran_source, full_path_driver_name = parse_cmd_line_args()
    driver_name = full_path_driver_name.split('/')[-1]

    modules, subroutines = parse_fortran_source(fortran_source)
    driver_string = generate_zofu_driver(driver_name, modules, subroutines, use_mpi)

    fid = open(full_path_driver_name, "w")
    fid.write(driver_string)
    fid.close()
    return


main()

import subprocess
import argparse
import sys
import os
import warnings
from pathlib import Path

from python.test_runner import settings
from python.parse.read_stdout import ResultType


def parse_test_options(argv):
    """
    Parse test options passed directly to python using argparse.
    Where settings are not specified, default values are assigned.

    This has been written to be used in conjunction with CMake variables.
    Some examples:

    Debug serial
        pytest -s tests/test.py --build_type ${CMAKE_BUILD_TYPE} "serial" --exe ${EXE_OUTPUT_NAME}

    MPI+openMP release
        pytest -s tests/test.py --build_type ${CMAKE_BUILD_TYPE} "hybrid" --exe ${EXE_OUTPUT_NAME}
            --np 2 --omp_num_threads 2

    The full executable path is determined from the build type.

    If the number of processes (np) or number of OMP threads (omp_num_threads)
    are not set, defaults defined in the settings module are used.

    See https://docs.python.org/3.3/library/argparse.html
    16.4.3. The add_argument() method¶  for more details on argparse.

    TODO
        1. Consider replacing hybrid with omp mpi
        2. add_argument settings should use those in conftest.py settings, else
           defining the same things in two places (dangerous shadowing)

    :param: argsv, subset of sys.argv, which should only contain the options
            used by the test driver.
    :return: args, parsed arguments.
    """
    parser = argparse.ArgumentParser(description='Run an application test.')

    parser.add_argument('--build_type',
                        type=str,
                        dest='build_type',
                        nargs=2,
                        default=['debug', 'serial'],
                        choices=['debug', 'release', 'relwithdebinfo', 'minsizerel',
                                 'serial', 'omp', 'mpi', 'hybrid'],
                        help='Program build type and parallelism. For example, debug serial')

    parser.add_argument('--exe',
                        type=str,
                        dest='exe',
                        required=True,
                        help='Name of the executable (no path)')

    parser.add_argument('--np',
                        type=int,
                        dest='np',
                        default=None,
                        help='Number of MPI processes')

    parser.add_argument('--omp_num_threads',
                        type=int,
                        dest='omp_num_threads',
                        default=None,
                        help='Number of openMP threads')

    args = parser.parse_args(argv)

    # Consistency checks
    if 'serial' in args.build_type:
        assert args.np is None, "--np should not be set with serial build type"
        assert args.omp_num_threads is None, "--omp_num_threads should not be set with serial build type"
        args.omp_num_threads = settings.DefaultSerial.omp_num_threads

    if 'mpi' in args.build_type:
        assert args.omp_num_threads is None, \
            "--omp_num_threads should not be set with a pure MPI build type"
        if args.np is None:
            args.np = settings.DefaultPureMpi.np

    if 'omp' in args.build_type:
        assert args.np is None, \
            "--np should not be set with a pure OMP build type"
        if args.omp_num_threads is None:
            args.omp_num_threads = settings.DefaultThreaded.omp_num_threads

    if 'hybrid' in args.build_type:
        if args.np is None:
            args.np = settings.DefaultMpiAndThreaded.np
        if args.omp_num_threads is None:
            args.omp_num_threads = settings.DefaultMpiAndThreaded.omp_num_threads

    assert not ('mpi' in args.build_type and 'omp' in args.build_type), \
        "A hybrid MPI OMP build type is specified with the 'hybrid' keyword"

    # Note: Easier to not use the enums
    # Convert strings to enums
    # build_type_enums = settings.build_type_string_to_enum(args.build_type)
    #
    # run_settings['executable'] = \
    #     settings.set_full_executable(build_type_enums, args.exe)

    args.exe = settings.set_full_executable(args.build_type, args.exe)

    # Check things look ok:
    # print(args)

    return args


def run_executable(args, input_file) -> dict:
    """
    Run an executable. Assumes CMake build system

    See here for a more extensive way to manage the env:
    https://stackoverflow.com/questions/2059482/python-temporarily-modify-the-current-processs-environment

    :param args: command-line arguments for the build type (list), fortran executable (str)
                 MPI processes (int) and OMP threads (int).
    :param input: input file name, defining the program settings.
    :param build_type_string: build type str, as defined in CMake with ${CMAKE_BUILD_TYPE}
           and a variable for [serial, MPI, omp, hybrid].
    :param executable_name: Name of executable, as defined in CMake using
           RUNTIME_OUTPUT_NAME property of set_target_properties(...)
    :return: Dictionary containing stdout, stderr and returncode (error if not 0).
             The standard output and errors are lists, where each element is a string.
             (Conversion from a byte object has been performed)
    """
    try:
        Path(args.exe).resolve(strict=True)
    except FileNotFoundError as error:
        raise error

    os.environ["OMP_NUM_THREADS"] = str(args.omp_num_threads)
    run_command = ['./' + args.exe, input_file]

    if 'mpi' or 'hybrid' in args.build_type:
        run_command = ['mpirun', '-np', str(args.np)] + run_command

    process = subprocess.run(run_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if process.returncode != 0:
        warnings.warn('process returned to stderr: ' + " ".join(run_command))

    return {'stdout': process.stdout.decode("utf-8").split('\n'),
            'stderr': process.stderr.decode("utf-8").split('\n'),
            'returncode': process.returncode}


def setup(input_name: str):
    """
    Set up a job, run it and return the results

    :param input_name: fortran program input file
    :return: Results in ResultType object
    """
    try:
        Path(input_name).resolve(strict=True)
    except FileNotFoundError as error:
        raise error

    # Get executable location and run settings
    # TODO Get parsed command-line options used by the test runner (and not pytest)
    # rather than passing a hard-coded indexing which assumes the number of pytest args
    run_settings = parse_test_options(sys.argv[3:])

    # Run the code and return the output
    output = run_executable(run_settings, input_name)

    # Parse stdout into results object and return
    return ResultType(output['stdout'])

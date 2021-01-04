import subprocess
import argparse

from python.test_runner import settings


def parse_test_options():
    """
    Parse test options passed directly to python using argparse.
    Where settings are not specified, default values are assigned.
    The full executable path is determined from the build type.

    Written to be used in conjunction with CMake variables. Some examples:
    Debug serial
        python3 test.py --build_type ${CMAKE_BUILD_TYPE} "serial" --exe ${EXE_OUTPUT_NAME}

    MPI+openMP release
        python3 test.py --build_type ${CMAKE_BUILD_TYPE} "hybrid" --exe ${EXE_OUTPUT_NAME}
            --np 2 --omp_num_threads 2

    If the number of processes (np) or number of OMP threads (omp_num_threads)
    are not set, defaults defined in the settings module are used.

    See https://docs.python.org/3.3/library/argparse.html
        16.4.3. The add_argument() method¶
    for more details on argparse.

    TODO(Alex) Consider replacing hybrid with omp mpi

    :return: args, parsed arguments
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

    args = parser.parse_args()

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

    :param args
    :param input: input file name for executable
    :param build_type_string: build type str, as defined in CMake with ${CMAKE_BUILD_TYPE}
    :param executable_name: Name of executable, as defined in CMake using
           RUNTIME_OUTPUT_NAME property of set_target_properties(...)
    :return: Run code and return standard output
    """

    set_omp = ['export OMP_NUM_THREADS=' + str(args.omp_num_threads)]
    mpi_run = ['mpirun', '-np']
    run_command = [args.exe, input_file]

    if 'serial' or 'omp' in args.build_type:
        # Need to get set_omp to work
        #full_run_command = set_omp + run_command
        full_run_command = run_command

    elif 'mpi' or 'hybrid' in args.build_type:
        quit('Need to get set_omp to work')
        #full_run_command = set_omp + mpi_run + run_command

    print(full_run_command)
    quit('Quit after printing run command - fix subprocess')

    try:
         process = subprocess.run(full_run_command, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:  # as error:
         pass
         #print("subprocess error:", error.returncode, "found:", error.output)

    return process

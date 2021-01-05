"""
Description:
Required by pytest to pass custom command-line arguments.

This used because I want to launch the tests from CMake and CMake a) knows
the build type/path and b) will distinguish between serial and parallel tests.

Alternatively, one could have CMake use add_custom_command to write a file
that the python test can read the settings from.

Reference:
https://docs.pytest.org/en/stable/parametrize.html#basic-pytest-generate-tests-example

TODO(Alex) Turn addoptions into dictionaries or objects that can also
be used in python/test_runner/run.py
"""


def pytest_addoption(parser):
    """
    Custom command-line options parsed added to pytest.
    Function used by pytest.

    These are ONLY used in the test runner to determine the full path to
    the fortran executable and the run settings.
    """

    parser.addoption(
        '--build_type',
        type=str,
        dest='build_type',
        nargs=2,
        default=['debug', 'serial'],
        choices=['debug', 'release', 'relwithdebinfo', 'minsizerel',
                 'serial', 'omp', 'mpi', 'hybrid'],
        help='Program build type and parallelism. For example, debug serial'
                    )

    parser.addoption('--exe',
                     type=str,
                     dest='exe',
                     required=True,
                     help='Name of the executable (no path)'
                     )

    parser.addoption('--np',
                     type=int,
                     dest='np',
                     default=None,
                     help='Number of MPI processes'
                     )

    parser.addoption('--omp_num_threads',
                     type=int,
                     dest='omp_num_threads',
                     default=None,
                     help='Number of openMP threads'
                     )


def pytest_generate_tests(metafunc):
    """
    Add parameter or parameters to metafunc.
    Function used by pytest.

    :param metafunc: Look me up
    """
    for option in ['build_type', 'exe', 'np', 'omp_num_threads']:
        if option in metafunc.fixturenames:
            metafunc.parametrize(option, metafunc.config.getoption(option))

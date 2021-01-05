"""
--------------------------
Description
--------------------------
Required by pytest to pass custom command-line arguments.

This used because I want to launch the tests from CMake and this a) knows
the build type/path and b) will distinguish between serial and parallel tests.

Alternatively, one could have CMake use add_custom_command to write a file
that the python test can read the settings in from.

--------------------------
References
--------------------------
https://docs.pytest.org/en/stable/parametrize.html#basic-pytest-generate-tests-example

Answered in two places on Stack Exchange:
 *  https://stackoverflow.com/questions/60785825/how-to-pass-command-line-arguments-to-pytest-tests-running-in-vscode
 *  Lost the other that refers to using conftest

mock.patch sys.argsv could also be considered
 *  https://stackoverflow.com/questions/51710083/how-to-run-pytest-with-a-specified-test-directory-on-a-file-that-uses-argparse

More references on testing command-line arguments
 *  http://euccas.github.io/blog/20160807/python-unittest-handle-command-line-arguments.html
 *  https://stackoverflow.com/questions/40880259/how-to-pass-arguments-in-pytest-by-command-line
 *  https://stackoverflow.com/questions/54071312/how-to-pass-command-line-argument-from-pytest-to-code
 *  https://stackoverflow.com/questions/55259371/pytest-testing-parser-error-unrecognised-arguments


TODO(Alex) Turn addoptions into dictionaries or objects that can also
be used in python/test_runner/run.py
"""

_test_runner_custom_options = ['build_type', 'exe', 'np', 'omp_num_threads']


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
    for option in _test_runner_custom_options:
        if option in metafunc.fixturenames:
            metafunc.parametrize(option, metafunc.config.getoption(option))

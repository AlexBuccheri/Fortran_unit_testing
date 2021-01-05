# # Required by pytest to pass custom command-line arguments.
# # Means I need to the parser defined in two places
# # which makes no sense

def pytest_addoption(parser):



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
    custom_options = ['build_type', 'exe', 'np', 'omp_num_threads']

    for option in custom_options:
        if option in metafunc.fixturenames:
            metafunc.parametrize(option, metafunc.config.getoption(option))



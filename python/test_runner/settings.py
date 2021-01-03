"""
Settings for running tests
"""
import enum

@enum.unique
class BuildType(enum.Enum):
    DEBUG = enum.auto()
    RELEASE = enum.auto()
    RELWITHDEBUGINFO = enum.auto()
    MINSIZEREL = enum.auto()

@enum.unique
class ParallelisationType(enum.Enum):
    SERIAL = enum.auto()
    OMP = enum.auto()
    MPI = enum.auto()
    MPIANDTHREADED = enum.auto()


_build_type_strings = ['debug', 'release', 'minsizerel', 'relwithdebinfo']


class DefaultSerial:
    omp_num_threads = 1


class DefaultThreaded:
    omp_num_threads = 4


class DefaultPureMpi:
    np = 4


class DefaultMpiAndThreaded:
    omp_num_threads = 2
    np = 2


def set_full_executable(input_build_type: list, exe: str) -> str:
    """
    Given a build type and the executable name, get the full path to the
    appropriate executable - assuming CMake naming conventions for build
    directories.

    :param input_build_type: List of build type strings
    :param exe:  Executable name str
    :return: full path to executable str
    """

    # Discard parallelism information. Not required for specifying the build directory
    build_type = [b for b in input_build_type if b in _build_type_strings]

    assert len(build_type) == 1, \
        "Either zero, or more than one build type is specified in input_build_type"

    return "cmake-build-" + build_type[0] + "/bin/" + exe


def build_type_string_to_enum(input_build_type: list) -> BuildType:
    """
    Convert built type options to enums
    :param input_build_type: list containing built setting strings
    # TODO(Alex) Consider refactoring with dictionaries
    """
    build_type = []

    for string in input_build_type:
        if string.lower() == 'debug':
            build_type.append(BuildType.DEBUG)

        elif string.lower() == 'release':
            build_type.append(BuildType.RELEASE)

        elif string.lower() == 'minsizerel':
            build_type.append(BuildType.MINSIZEREL)

        elif string.lower() == 'relwithdebinfo':
            build_type.append(BuildType.RELWITHDEBUGINFO)

        elif string.lower() == 'serial':
            build_type.append(ParallelisationType.SERIAL)

        elif string.lower() == 'omp':
            build_type.append(ParallelisationType.OMP)

        elif string.lower() == 'mpi':
            build_type.append(ParallelisationType.MPI)

        elif string.lower() == 'hybrid':
            build_type.append(ParallelisationType.MPIANDTHREADED)

        else:
            exit("Build type string is erroneous:", string)

    return build_type


# def set_full_executable(input_build_type: list, exe_name: str) -> str:
#     """
#     Given a build type and the executable name, get the full path to the
#     appropriate executable - assuming CMake naming conventions for build
#     directories.
#
#     :param build_type: Build type list containing enums,
#            such as ['BuildType.DEBUG', 'ParallelisationType.SERIAL']
#     :param exe_name:  Executable name str
#     :return: full path to executable str
#     """
#     build_types = [entry for entry in BuildType]
#
#     # Discard parallelism information. Not required for specifying build directory
#     build_type = [b for b in input_build_type if b in build_types]
#
#     assert len(build_type) == 1, \
#         "Either zero, or more than one build type specified in input_build_type"
#
#     # TODO(ALEX) One would need to convert back to a string for build_type[0]
# executable = {
#     BuildType.DEBUG: "cmake-build-debug/bin/" + exe_name,
#     BuildType.RELEASE: "cmake-build-release/bin/" + exe_name,
#     BuildType.RELWITHDEBUGINFO: "cmake-build-minsizerel/bin/" + exe_name,
#     BuildType.MINSIZEREL: "cmake-build-relwithdebinfo/bin/" + exe_name
# }
#     return "cmake-build-" + build_type[0] + "/bin/" + exe_name





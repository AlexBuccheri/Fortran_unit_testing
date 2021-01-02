"""

Settings for running tests

Choose the only executable - Should pass from the CMake file

"""
import enum

@enum.unique
class BuildType(enum.Enum):
    DEBUG          = enum.auto()
    RELEASE        = enum.auto()
    RELWITHDEBUGINFO = enum.auto()
    MINSIZEREL     = enum.auto()

@enum.unique
class ParallelisationType(enum.Enum):
    SERIAL         = enum.auto()
    THREADED       = enum.auto()
    PUREMPI        = enum.auto()
    MPIANDTHREADED = enum.auto()



#class TestSettings():



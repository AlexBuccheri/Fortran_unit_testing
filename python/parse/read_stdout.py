import numpy as np


class ResultType:
    """
    Basic container to hold results
    Dictionary might be better
    """
    def __init__(self, stdout: list):
        self.distance_matrix = self.extract_distance_matrix(stdout)
        self.n_atoms = self.distance_matrix.shape[0]

    def extract_distance_matrix(self, stdout: list):
        """
        Disgusting routine but does the job for demo purposes
        Assumes specific, fixed structure for the output of the fortran code
        Would be better to use structured output, like json

        :param stdout: Standard output in a list (line-separated)
        :return: distance matrix, d
        """
        assert type(stdout) == list, "expect stdout as a list of strings"

        n = int(np.sqrt(len(stdout[3:-1])))
        d = np.empty(shape=(n, n))

        for line in stdout[3:-1]:
            i, j, d_value = line.split()
            # Fortran to python indexing
            d[int(i)-1, int(j)-1] = d_value

        return d

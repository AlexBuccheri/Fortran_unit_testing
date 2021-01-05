# External python packages
import unittest
import numpy as np
import scipy.spatial
import sys

# Our python packages: Test runner for this project
from python.test_runner.run import setup
from python.parse.read_stdout import ResultType

def output_co2_xyz(input_name):
    """
    Helper routine to write CO2 xyz to file
    Data ref: http://www.chm.bris.ac.uk/~paulmay/temp/pcc/co2symstretch.htm

    :param input_name: file nam e
    :return: Write input_name to file in xyz format
    """
    co2_xyz = """3 
  
C  0.0000000   0.0000000   0.0000000
O  0.0000000   0.0000000   1.5140760
O  0.0000000   0.0000000  -1.5140760
    """
    fid = open(input_name, "w")
    fid.write(co2_xyz)
    fid.close()
    return


class MyTestCase(unittest.TestCase):
    """
    Application test for CO2 distance matrix
    To run manually:
      pytest -s tests/co2_distance_matrix.py --build_type serial debug --exe unit_testing
    """

    def test_co2_distance_matrix(self):
        """
        Test description: Molecular CO2 distance matrix


        :param self: pytest object
        """
        # Specify input file
        input_name = 'co2_distance_matrix.in'

        # Standard setup used to run all app tests and return parsed results
        result = setup(input_name)

        # Parse reference result from file, if available
        #    ELSE define in the test
        ref_result = None

        self.assertEqual(result.n_atoms, 3, "Number of atoms in molecule")

        self.assertEqual(result.distance_matrix.shape[0],
                         result.distance_matrix.shape[1],
                         "Distance matrix is not square")

        # TODO(Alex) Look at how to compare arrays in pytest
        self.assertTrue(np.allclose(result.distance_matrix,
                                    result.distance_matrix.transpose(),
                                    atol=1.e-8),
                        msg="Distance matrix is not square")

        ref_pos = np.array([[0.0000000,   0.0000000,   0.0000000],
                            [0.0000000,   0.0000000,   1.5140760],
                            [0.0000000,   0.0000000,  -1.5140760]])
        ref_distance_matrix = scipy.spatial.distance_matrix(ref_pos, ref_pos)

        self.assertTrue(np.allclose(result.distance_matrix,
                                    ref_distance_matrix,
                                    atol=1.e-8),
                        msg="CO2 distance matrix")


if __name__ == '__main__':
    unittest.main()

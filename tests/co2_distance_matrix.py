# External python packages
# pytest supports unittest.Testcase
import unittest
import numpy as np
import scipy.spatial

# Our python packages: Test runner for this project
# TODO(Alex) Think about the best way to deal with this
# https://stackoverflow.com/questions/16114391/adding-directory-to-sys-path-pythonpath
# https://stackoverflow.com/questions/10095037/why-use-sys-path-appendpath-instead-of-sys-path-insert1-path
import sys
sys.path.insert(1,'/Users/alexanderbuccheri/CLionProjects/unit_testing/')
from python.test_runner.run import setup


class MyTestCase(unittest.TestCase):
    """
    Application test for CO2 distance matrix
    To run manually:
      pytest -s tests/co2_distance_matrix.py --build_type serial debug --exe unit_testing

    TODO
      1. Note, I'm writing the test with unittest, not pytest
         It might be better to purely use pytest and reduce complexity + dependencies
      2. Look at how to compare arrays in unittest or pytest, rather than using numpy
        (which somewhat defeats the point of using pytest)
    """

    # Specify input file (in this example, nothing more than an xyz file)
    input_name = 'co2_distance_matrix.in'

    # Standard setup used to run all app tests and return parsed results
    result = setup(input_name)

    # Parse reference result from file OR define refs in the test
    ref_result = None

    # First application test
    def test_co2_distance_matrix(self):

        result = self.result

        self.assertEqual(result.n_atoms, 3, "Number of atoms in molecule")

        self.assertEqual(result.distance_matrix.shape[0],
                         result.distance_matrix.shape[1],
                         "Distance matrix is not square")

        self.assertTrue(np.allclose(result.distance_matrix,
                                    result.distance_matrix.transpose(),
                                    atol=1.e-8),
                        msg="Distance matrix is not symmetric")

        ref_pos = np.array([[0.0000000,   0.0000000,   0.0000000],
                            [0.0000000,   0.0000000,   1.5140760],
                            [0.0000000,   0.0000000,  -1.5140760]])
        ref_distance_matrix = scipy.spatial.distance_matrix(ref_pos, ref_pos)

        self.assertTrue(np.allclose(result.distance_matrix,
                                    ref_distance_matrix,
                                    atol=1.e-8),
                        msg="CO2 distance matrix")

    # Other application tests


if __name__ == '__main__':
    unittest.main()


def output_co2_xyz(input_name):
    """
    Helper routine to write CO2 xyz to file
    Data ref: http://www.chm.bris.ac.uk/~paulmay/temp/pcc/co2symstretch.htm

    :param input_name: file name
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
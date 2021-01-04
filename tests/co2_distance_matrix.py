# External python packages
import unittest

# Our python packages: Test runner for this project
from python.test_runner.run import parse_test_options, run_executable


class MyTestCase(unittest.TestCase):
    """
    Application tests for CO2 distance matrix
    """

    # Specify input file or generate the input file
    input_name = 'co2_distance_matrix.in'

    # http://www.chm.bris.ac.uk/~paulmay/temp/pcc/co2symstretch.htm
    co2_xyz = """3 
  
C  0.0000000   0.0000000   0.0000000
O  0.0000000   0.0000000   1.5140760
O  0.0000000   0.0000000  -1.5140760
    """
    fid = open(input_name, "w")
    fid.write(co2_xyz)
    fid.close()

    # Get executable location and run settings
    run_settings = parse_test_options()

    # Run the code and return output to stdout
    std_out = run_executable(run_settings, input_name)


    # An application test
    def test_co2_distance_matrix(self):
        """
        Test description: Molecular CO2 distance matrix
        """

        # Parse reference data OR have it defined here
        self.assertEqual(1, 1)

    # Add more application tests here


if __name__ == '__main__':
    unittest.main()

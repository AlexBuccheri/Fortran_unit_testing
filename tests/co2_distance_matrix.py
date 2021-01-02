# External python packages
import unittest
import sys

# Our python packages: Test runner for this project
import python.test_runner.settings
from python.test_runner.run import run_qcore


class MyTestCase(unittest.TestCase):
    """
    Application tests for CO2 distance matrix
    """

    # Specify input file
    input = 'c02_distance_matrix.in'

    # Get executable location and run settings (assume only serial for now)
    #sort the cmake directoires

    # Run the code
    run_qcore()

    # Parse output

    # Parse reference data OR have it defined here

    def test_co2_distance_matrix(self):
        self.assertEqual(1, 1)



if __name__ == '__main__':
    unittest.main()

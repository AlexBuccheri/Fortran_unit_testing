# External python packages
import unittest

# Our python packages: Test runner for this project
from python.test_runner.run import parse_test_options, run_executable


class MyTestCase(unittest.TestCase):
    """
    Application tests for CO2 distance matrix
    """

    # Specify input file or generate the input file
    input = 'c02_distance_matrix.in'

    # Get executable location and run settings
    run_settings = parse_test_options()

    # Run the code
    std_out = run_executable(run_settings, input)

    # Parse output: Result written to std out

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

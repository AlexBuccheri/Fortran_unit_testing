Application Tests with Pytest

  Application tests in this project use python's Pytest as the test runner.
  A test is run within the unittest class, and functions defined within the
  class can assert the binary's output.

  Every application test needs to run the same four commands:  
  
    *  Get the input file name from the command line
       (or have the app test write one)

    *  Get the test run-settings from the command line:
         - binary type
         - number of cores
         - number of threads
       else use the defaults

    * Run the test with the defined settings and input
        - Check the run succeeded

    * Read in the output from results file

  One can then assert on the generated data.

  The advantages of using pytest over a more dedicated app test framework:  
  
    * Excellent support: I don't expect support for pytest development to be
        dropped any time soon.
    * Lightweight: Requires a minimal amount of code to set up a test, and one
        can do everything from within python.
    * Convenient: Do everything in one place and take advantage of existing
        python libraries. Can also run everything within a virtual env => clean.
    * High-level assertions: One isn't restricted to comparing scalars or arrays.
        Indeed, one could write more complex tests where required. And do so easily
        with numpy and scipy (data interpolation, statistical analysis etc).
        Also the possibility to use symbolic maths via sympy.
    * Easy generation of input files:
        For any code with python ASE support, one can easily set up crystal
        structures from CIFs to the required format.
        Also makes for easier integration with the NOMAD database
    * Utilise python documentation.
    * Flexible: https://docs.pytest.org/en/stable/assert.html
        Reference data can be stored in the python tester or as a reference file.

  Disadvantages:  
  
    * Proliferation of files: Writing test assertions separately from test input is always more dangerous
    * Can result in multiple python dependencies - Negated by setting up a virtual env
    * Maybe this can all be done more simply and cleanly with a dedicated app test framework? 
    * More may become apparent 

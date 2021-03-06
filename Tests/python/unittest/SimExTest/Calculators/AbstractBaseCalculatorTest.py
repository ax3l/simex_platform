##########################################################################
#                                                                        #
# Copyright (C) 2015 Carsten Fortmann-Grote                              #
# Contact: Carsten Fortmann-Grote <carsten.grote@xfel.eu>                #
#                                                                        #
# This file is part of simex_platform.                                   #
# simex_platform is free software: you can redistribute it and/or modify #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# simex_platform is distributed in the hope that it will be useful,      #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                        #
##########################################################################

""" Test module for the AbstractBaseCalculator module.

    @author : CFG
    @institution : XFEL
    @creation 20151006

"""
import paths
import unittest
import exceptions
import os


# Import the class to test.
from SimEx.Calculators.AbstractBaseCalculator import AbstractBaseCalculator
from SimEx.Calculators.AbstractBaseCalculator import checkAndSetIO
from SimEx.Calculators.AbstractBaseCalculator import checkAndSetParameters
from SimEx.Parameters.AbstractCalculatorParameters import AbstractCalculatorParameters

# Test parameter class.
class DerivedParameters(AbstractCalculatorParameters):
    def __init__(self, a, b, c):
        self.__a = a
        self.__b = b
        self.__c = c

# Derive a class from the abc.
class DerivedCalculator(AbstractBaseCalculator):
    def __init__(self, parameters=None, input_path=None, output_path=None):
        super(DerivedCalculator, self).__init__(parameters, input_path, output_path)
    def backengine(self):
        pass
    def _readH5(self):
        pass
    def saveH5(self):
        pass
    def providedData(self):
        return ['/params/params1', '/params/params2', '/data/dat1', '/data/dat2']
    def expectedData(self):
        return ['/data/dat1', '/data/dat2']


class AbstractBaseCalculatorTest(unittest.TestCase):
    """
    Test class for the AbstractBaseCalculator.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """

    def setUp(self):
        """ Setting up a test. """
        self.__files_to_be_removed = []

        self.test_class_instance = DerivedCalculator(parameters={1 : '1'}, input_path=__file__, output_path='test.h5')

    def tearDown(self):
        """ Tearing down a test. """
        for f in self.__files_to_be_removed:
            if os.path.isfile(f): os.remove(f)

        del self.test_class_instance


    def testConstruction(self):
        """ Testing the default construction of the class. """
        self.assertRaises(TypeError, AbstractBaseCalculator )

    def testConstructionParametersDict(self):
        """ Testing the construction of the class with a parameters dict. """
        abc =  DerivedCalculator( parameters={},
                                  input_path=__file__,
                                  output_path='out.h5' )

        self.assertIsInstance( abc, AbstractBaseCalculator )

    def testConstructionParametersClass(self):
        """ Testing the construction with a parameters class instance. """
        abc =  DerivedCalculator( parameters=DerivedParameters(1,2,3),
                                  input_path=__file__,
                                  output_path='out.h5' )

        self.assertIsInstance( abc, AbstractBaseCalculator )

    # Check its type.
    def testQueries(self):

        abc = self.test_class_instance
        # Check it has the required members.
        self.assertTrue( hasattr(abc, 'parameters') )
        self.assertTrue( hasattr(abc, 'input_path') )
        self.assertTrue( hasattr(abc, 'output_path') )


    def testCheckAndSetIO(self):
        """ Check that setting data io paths works correctly. """
        inp = 'test.in'
        out = 'test.out'
        # Ensure proper cleanup.
        self.__files_to_be_removed += [inp, out]

        # Setup the tuple.
        io = (inp, out)

        # Create a dummy input file.
        inp_handle = open(inp, 'w')
        inp_handle.write('xxx')
        inp_handle.close()

        # Call checker.
        io_ret = checkAndSetIO(io)

        self.assertEqual(io_ret[0], os.path.abspath(inp) )
        self.assertEqual(io_ret[1], os.path.abspath(out) )

        # Check exception on wrong types.
        io = (1,2)
        self.assertRaises(exceptions.TypeError, checkAndSetIO, io )

        # Check exception on wrong second type.
        io = ('test.in', 2)
        self.assertRaises(exceptions.TypeError, checkAndSetIO, io )

        # Check exception on wrong second type.
        io = ('test.in', None)
        self.assertRaises(exceptions.IOError, checkAndSetIO, io )

    def testProvidedData(self):
        """ Check the provided data query. """

        instance = self.test_class_instance
        provided_data = instance.providedData()
        expected_data = instance.expectedData()

        for ed in expected_data:
            self.assertTrue ( ed in provided_data)

    def testCheckAndSetParameters(self):
        """ Test the parameters check'n'set function. """
        # Check default.
        self.assertEqual( {}, checkAndSetParameters( None ) )

        # Check exceptions on wrong type.
        self.assertRaises( TypeError, checkAndSetParameters, [1,2,3] )
        self.assertRaises( TypeError, checkAndSetParameters, 1 )
        self.assertRaises( TypeError, checkAndSetParameters, 'string of parameters' )
        self.assertRaises( TypeError, checkAndSetParameters, ['list', 'of', 'parameters'] )

        # Check return from correct input.
        parameters = DerivedParameters(a=1, b=2, c=3)
        self.assertEqual( parameters, checkAndSetParameters( parameters ) )

if __name__ == '__main__':
    unittest.main()


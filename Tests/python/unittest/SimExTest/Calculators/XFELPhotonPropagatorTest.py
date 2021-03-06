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
# Include needed directories in sys.path.                                #
#                                                                        #
##########################################################################

""" Test module for the XFELPhotonPropagator.

    @author : CFG
    @institution : XFEL
    @creation 20151104

"""
import os, shutil
import paths
import unittest

import numpy
import h5py

# Import the class to test.
from SimEx.Calculators.XFELPhotonPropagator import XFELPhotonPropagator
from TestUtilities import TestUtilities

class XFELPhotonPropagatorTest(unittest.TestCase):
    """
    Test class for the XFELPhotonPropagator class.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """
        cls.input_h5 = TestUtilities.generateTestFilePath('FELsource_out/FELsource_out_0000000.h5')

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """

    def setUp(self):
        """ Setting up a test. """
        self.__files_to_remove = []
        self.__dirs_to_remove = []

    def tearDown(self):
        """ Tearing down a test. """

        for f in self.__files_to_remove:
            if os.path.isfile(f): os.remove(f)
        for d in self.__dirs_to_remove:
            if os.path.isdir(d): shutil.rmtree(d)


    def testConstruction(self):
        """ Testing the default construction of the class. """

        # Construct the object.
        xfel_propagator = XFELPhotonPropagator(parameters=None, input_path=self.input_h5, output_path='prop_out_0000000.h5')


        self.assertIsInstance(xfel_propagator, XFELPhotonPropagator)

    @unittest.skip("Skipped")
    def testConstructionNumberOfFiles(self):
        """ Test that input and output are setup correctly depending on the number and type of input files given."""
        ### TODO
        self.assertTrue(False)

    def testBackengineSingleInputFile(self):
        """ Test a backengine run with a single input file. """
        # Construct the object.
        xfel_propagator = XFELPhotonPropagator( parameters=None, input_path=self.input_h5, output_path='prop_out_0000001.h5' )

        # Call the backengine.
        status = xfel_propagator.backengine()

        # Check backengine returned sanely.
        self.assertEqual( status, 0 )

        # Ensure clean-up.
        self.__files_to_remove.append(xfel_propagator.output_path)

    def testBackengineMultipleInputFile(self):
        """ Test a backengine run with multiple input files. """
        # Construct the object.
        xfel_propagator = XFELPhotonPropagator( parameters=None, input_path=TestUtilities.generateTestFilePath( 'FELsource_out' ), output_path='prop_out' )

        # Call the backengine.
        status = xfel_propagator.backengine()

        # Check backengine returned sanely.
        self.assertEqual( status, 0 )

        # Ensure clean-up.
        self.__dirs_to_remove.append(xfel_propagator.output_path)



if __name__ == '__main__':
    unittest.main()


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

""" Test module for the SingFELPhotonDiffractor.

    @author : CFG
    @institution : XFEL
    @creation 20151109

"""
import os
import shutil
import subprocess

# Include needed directories in sys.path.
import paths
import unittest


# Import the class to test.
from SimEx.Calculators.SingFELPhotonDiffractor import SingFELPhotonDiffractor
from TestUtilities import TestUtilities

class SingFELPhotonDiffractorTest(unittest.TestCase):
    """
    Test class for the SingFELPhotonDiffractor class.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """
        cls.input_h5 = TestUtilities.generateTestFilePath('pmi_out_0000001.h5')

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """
        del cls.input_h5

    def setUp(self):
        """ Setting up a test. """
        self.__files_to_remove = []
        self.__dirs_to_remove = []

    def tearDown(self):
        """ Tearing down a test. """
        for f in self.__files_to_remove:
            if os.path.isfile(f):
                os.remove(f)
        for d in self.__dirs_to_remove:
            if os.path.isdir(d):
                shutil.rmtree(d)

    def testConstruction(self):
        """ Testing the default construction of the class. """

        parameters={ 'uniform_rotation': True,
                     'calculate_Compton' : False,
                     'slice_interval' : 100,
                     'number_of_slices' : 2,
                     'pmi_start_ID' : 1,
                     'pmi_stop_ID'  : 1,
                     'number_of_diffraction_patterns' : 2,
                     'beam_parameter_file' : TestUtilities.generateTestFilePath('s2e.beam'),
                     'beam_geometry_file' : TestUtilities.generateTestFilePath('s2e.geom'),
                   }

        # Construct the object.
        diffractor = SingFELPhotonDiffractor(parameters=parameters, input_path=self.input_h5, output_path='diffr_out.h5')

        self.assertIsInstance(diffractor, SingFELPhotonDiffractor)

    def testConstructionExceptions(self):
        """ Check that proper exceptions are thrown if object is constructed incorrectly. """
        # Parameter not a dict.
        self.assertRaises( TypeError, SingFELPhotonDiffractor, 1, self.input_h5, 'diffr.h5')

        # Setup parameters that are ok
        parameters={ 'uniform_rotation': True,
                     'calculate_Compton' : False,
                     'slice_interval' : 100,
                     'number_of_slices' : 2,
                     'pmi_start_ID' : 1,
                     'pmi_stop_ID'  : 1,
                     'number_of_diffraction_patterns' : 2,
                     'beam_parameter_file' : TestUtilities.generateTestFilePath('s2e.beam'),
                     'beam_geometry_file' : TestUtilities.generateTestFilePath('s2e.geom'),
                     }

        # Check construction with sane parameters.
        singfel = SingFELPhotonDiffractor( parameters, self.input_h5, 'diffr.h5')
        self.assertIsInstance( singfel, SingFELPhotonDiffractor )

        # uniform_rotation not a bool.
        parameters['uniform_rotation'] = 1
        self.assertRaises( TypeError, SingFELPhotonDiffractor, parameters, self.input_h5, 'diffr.h5')
        # Reset.
        parameters['uniform_rotation'] = True

        # calculate_Compton not a bool.
        parameters['calculate_Compton'] = 1
        self.assertRaises( TypeError, SingFELPhotonDiffractor, parameters, self.input_h5, 'diffr.h5')
        # Reset.
        parameters['calculate_Compton'] = False

        # slice_interval not positive integer.
        parameters['slice_interval'] = -1
        self.assertRaises( TypeError, SingFELPhotonDiffractor, parameters, self.input_h5, 'diffr.h5')
        # slice_interval not a number
        parameters['slice_interval'] = 'one'
        self.assertRaises( TypeError, SingFELPhotonDiffractor, parameters, self.input_h5, 'diffr.h5')
        # Reset.
        parameters['slice_interval'] = 1

        # number_of_slices not positive integer.
        parameters['number_of_slices'] = -1
        self.assertRaises( TypeError, SingFELPhotonDiffractor, parameters, self.input_h5, 'diffr.h5')
        # number_of_slices not a number
        parameters['number_of_slices'] = 'one'
        self.assertRaises( TypeError, SingFELPhotonDiffractor, parameters, self.input_h5, 'diffr.h5')
        # Reset.
        parameters['number_of_slices'] = 2

        # number_of_diffraction_patterns not positive integer.
        parameters['number_of_diffraction_patterns'] = -1
        self.assertRaises( TypeError, SingFELPhotonDiffractor, parameters, self.input_h5, 'diffr.h5')
        # number_of_diffraction_patterns not a number
        parameters['number_of_diffraction_patterns'] = 'one'
        self.assertRaises( TypeError, SingFELPhotonDiffractor, parameters, self.input_h5, 'diffr.h5')
        # Reset.
        parameters['number_of_diffraction_patterns'] = 2

        # pmi_start_ID not positive integer.
        parameters['pmi_start_ID'] = -1
        self.assertRaises( TypeError, SingFELPhotonDiffractor, parameters, self.input_h5, 'diffr.h5')
        # pmi_start_ID not a number
        parameters['pmi_start_ID'] = 'one'
        self.assertRaises( TypeError, SingFELPhotonDiffractor, parameters, self.input_h5, 'diffr.h5')
        # Reset.
        parameters['pmi_start_ID'] = 1

        # pmi_stop_ID not positive integer.
        parameters['pmi_stop_ID'] = -1
        self.assertRaises( TypeError, SingFELPhotonDiffractor, parameters, self.input_h5, 'diffr.h5')
        # pmi_stop_ID not a number
        parameters['pmi_stop_ID'] = 'one'
        self.assertRaises( TypeError, SingFELPhotonDiffractor, parameters, self.input_h5, 'diffr.h5')
        # Reset.
        parameters['pmi_stop_ID'] = 1

        # beam_parameter_file not a string.
        parameters['beam_parameter_file'] = 1
        self.assertRaises( TypeError, SingFELPhotonDiffractor, parameters, self.input_h5, 'diffr.h5')
        # beam_parameter_file not a file.
        parameters['beam_parameter_file'] = 's2e.beam'
        self.assertRaises( IOError, SingFELPhotonDiffractor, parameters, self.input_h5, 'diffr.h5')
        parameters['beam_parameter_file'] =  TestUtilities.generateTestFilePath('s2e.beam')

        # beam_geometry_file not a string.
        parameters['beam_geometry_file'] = 1
        self.assertRaises( TypeError, SingFELPhotonDiffractor, parameters, self.input_h5, 'diffr.h5')
        # beam_geometry_file not a file.
        parameters['beam_geometry_file'] = 's2e.geom'
        self.assertRaises( IOError, SingFELPhotonDiffractor, parameters, self.input_h5, 'diffr.h5')
        parameters['beam_geometry_file'] =  TestUtilities.generateTestFilePath('s2e.geom'),

        # Unknown parameter name.
        parameters['number_of_nonexisting_parameter'] = 3
        self.assertRaises( RuntimeError, SingFELPhotonDiffractor, parameters, self.input_h5, 'diffr.h5')


    def testBackengine(self):
        """ Test that we can start a test calculation. """

        # Cleanup.
        self.__dirs_to_remove.append('diffr')

        parameters={ 'uniform_rotation': True,
                     'calculate_Compton' : False,
                     'slice_interval' : 100,
                     'number_of_slices' : 2,
                     'pmi_start_ID' : 1,
                     'pmi_stop_ID'  : 1,
                     'number_of_diffraction_patterns' : 2,
                     'beam_parameter_file' : TestUtilities.generateTestFilePath('s2e.beam'),
                     'beam_geometry_file' : TestUtilities.generateTestFilePath('s2e.geom'),
                     }

        # Construct the object.
        diffractor = SingFELPhotonDiffractor(parameters=parameters, input_path=self.input_h5, output_path='diffr')

        # Call backengine.
        status = diffractor.backengine()

        # Check successful completion.
        self.assertEqual(status, 0)

    def testBackengineInputFile(self):
        """ Test that we can start a test calculation if the input path is a single file. """

        # Cleanup.
        self.__dirs_to_remove.append('diffr')

        parameters={ 'uniform_rotation': True,
                     'calculate_Compton' : False,
                     'slice_interval' : 100,
                     'number_of_slices' : 2,
                     'pmi_start_ID' : 1,
                     'pmi_stop_ID'  : 1,
                     'number_of_diffraction_patterns' : 2,
                     'beam_parameter_file' : TestUtilities.generateTestFilePath('s2e.beam'),
                     'beam_geometry_file' : TestUtilities.generateTestFilePath('s2e.geom'),
                     }

        # Construct the object.
        diffractor = SingFELPhotonDiffractor(parameters=parameters, input_path=self.input_h5, output_path='diffr')

        # Call backengine.
        status = diffractor.backengine()

        # Check successful completion.
        self.assertEqual(status, 0)

    def testBackengineInputDir(self):
        """ Test that we can start a test calculation if the input path is a directory. """

        # Cleanup.
        self.__dirs_to_remove.append('diffr')

        parameters={ 'uniform_rotation': True,
                     'calculate_Compton' : False,
                     'slice_interval' : 100,
                     'number_of_slices' : 2,
                     'pmi_start_ID' : 1,
                     'pmi_stop_ID'  : 1,
                     'number_of_diffraction_patterns' : 2,
                     'beam_parameter_file' : TestUtilities.generateTestFilePath('s2e.beam'),
                     'beam_geometry_file' : TestUtilities.generateTestFilePath('s2e.geom'),
                     }

        # Construct the object.
        diffractor = SingFELPhotonDiffractor(parameters=parameters, input_path=os.path.dirname( self.input_h5 ), output_path='diffr')

        # Call backengine.
        status = diffractor.backengine()

        # Check successful completion.
        self.assertEqual(status, 0)

if __name__ == '__main__':
    unittest.main()


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

""" Module that holds the OrientAndPhasePhotonAnalyzer class.

    @author : CFG
    @institution : XFEL
    @creation 20151112

"""
from SimEx.Calculators.AbstractPhotonAnalyzer import AbstractPhotonAnalyzer

class OrientAndPhasePhotonAnalyzer(AbstractPhotonAnalyzer):
    """
    Class representing photon data analyzes that combines orientation and phasing of 2D diffraction data.
    """

    def __init__(self,  parameters=None, input_path=None, output_path=None):
        """
        Constructor for the photon analyzer.

        @param  :
        <br/><b>type</b> :
        <br/><b>default</b> :
        """

        # Initialize base class.
        super(OrientAndPhasePhotonAnalyzer, self).__init__(parameters,input_path,output_path)

        self.__provided_data = []

        self.__expected_data = []


    def expectedData(self):
        """ Query for the data expected by the Analyzer. """
        return self.__expected_data

    def providedData(self):
        """ Query for the data provided by the Analyzer. """
        return self.__provided_data

    def backengine(self):
        """ This method drives the backengine code."""
        pass

    @property
    def data(self):
        """ Query for the field data. """
        return self.__data

    def _readH5(self):
        """ """
        """ Private method for reading the hdf5 input and extracting the parameters and data relevant to initialize the object. """
        pass # Nothing to be done since IO happens in backengine.

        ## Read the file.
        #file_handle = h5py.File(self.input_path, 'r')

        ## Setup empty dictionary.
        #parameters = {}

        ## Get photon energy.
        ##parameters['photon_energy'] = file_handle['params/photonEnergy'].value

        ## Read the electric field data and convert to numpy array.
        #Ehor = numpy.array(file_handle['/data/arrEhor'][:])
        #Ever = numpy.array(file_handle['/data/arrEver'][:])

        ## Store on object.
        #self.__e_field = numpy.array([Ehor, Ever])

        #super(OrientAndPhasePhotonAnalyzer, self).__init__(parameters,self.input_path,self.output_path)

        #file_handle.close()

    def saveH5(self):
        """ """
        """
        Private method to save the object to a file.

        @param output_path : The file where to save the object's data.
        <br/><b>type</b> : string
        <br/><b>default</b> : None
        """
        pass # No action required since output is written in backengine.

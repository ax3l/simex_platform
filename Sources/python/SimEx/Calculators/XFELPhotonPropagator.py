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

""" Module that holds the XFELPhotonPropagator class.

    @author : CFG
    @institution : XFEL
    @creation 20151104

"""
import os

from prop import propagateSE

from SimEx.Calculators.AbstractPhotonPropagator import AbstractPhotonPropagator


class XFELPhotonPropagator(AbstractPhotonPropagator):
    """
    Class representing a x-ray free electron laser photon propagator.
    """

    def __init__(self,  parameters=None, input_path=None, output_path=None):
        """
        Constructor for the xfel photon propagator.

        @param  parameters  : Parameters steering the propagation of photons.
        <br/><b>type</b>               : dict

        @param  input_path  : Location of input data for the photon propagation.
        <br/><b>type</b>               : string

        @param  output_path : Location of output data for the photon propagation.
        <br/><b>type</b>               : string
        """

        # Initialize base class.
        super(XFELPhotonPropagator, self).__init__(parameters,input_path,output_path)


    def backengine(self):
        """ This method drives the backengine code, in this case the WPG interface to SRW."""

        # Check if input path is a directory.
        if os.path.isdir(self.input_path):
            input_files = [ os.path.join( self.input_path, input_file ) for \
                            input_file in os.listdir( self.input_path ) ]
            input_files.sort() # Assuming the filenames have some kind of ordering scheme.
        else:
            propagateSE.propagate(self.input_path, self.output_path)
            return 0

        # If we have more than one input file, we should also have more than one output file, i.e.
        # output_path should be a directory.
        if os.path.isfile(self.output_path):
            raise IOError("The given output path is a file but a directory is needed. Cowardly refusing to overwrite.")

        # Check if output dir exists, create if not.
        if not os.path.isdir(self.output_path):
            os.mkdir(self.output_path)

        # Loop over all input files and generate one run per source file.
        for i,input_file in enumerate(input_files):
            ### TODO: Transmit number of cpus.
            output_file = os.path.join( self.output_path, 'prop_out_%07d.h5' % (i) )
            propagateSE.propagate(input_file, output_file)

        return 0

        ### TODO: Consider moving IO logic to the ABC.

    @property
    def data(self):
        """ Query for the field data. """
        return self.__data

    def _readH5(self):
        """ """
        """ Private method for reading the hdf5 input and extracting the parameters and data relevant to initialize the object. """
        pass # Nothing to be done since IO happens in backengine.

    def saveH5(self):
        """ """
        """
        Private method to save the object to a file.

        @param output_path : The file where to save the object's data.
        <br/><b>type</b> : string
        <br/><b>default</b> : None
        """
        pass # No action required since output is written in backengine.

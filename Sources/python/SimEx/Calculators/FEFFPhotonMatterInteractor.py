""" :module FEFFPhotonMatterInteractor: Holds the FEFFPhotonMatterInteractor class."""
##########################################################################
#                                                                        #
# Copyright (C) 2015, 2016 Carsten Fortmann-Grote                        #
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

import h5py
import numpy
import os
import shutil
import stat
import subprocess
import tempfile

from distutils.spawn import find_executable

from SimEx.Calculators.AbstractPhotonInteractor import AbstractPhotonInteractor

class FEFFPhotonMatterInteractor(AbstractPhotonInteractor):
    """
    :class FEFFPhotonMatterInteractor: Interface class for photon-matter interaction calculations using the FEFF code.
    """

    def __init__(self,  parameters=None, input_path=None, output_path=None):
        """

        :param parameters: Parameters that govern the PMI calculation.
        :type parameters: FEFFPhotonMatterInteractorParameters

        :param input_path: Location of data needed by the PMI calculation.
        :type input_path: str

        :param output_path: Where to store the data generated by the PMI calculation.
        :type output_path: str
        """

        # Handle default output_path
        if output_path is None:
            if not os.path.exists('pmi'):
                os.mkdir('pmi')
            if os.path.isfile( 'pmi' ):
                raise IOError( "A file named 'pmi' already exists, cowardly refusing to overwrite.")
            output_path = 'pmi/pmi_out_0000001.h5'

        # Initialize base class.
        super(FEFFPhotonMatterInteractor, self).__init__(parameters,input_path,output_path)

        self.__provided_data = []

        self.__expected_data = ['/data/arrEhor',
                                '/data/arrEver',
                                '/params/Mesh/nSlices',
                                '/params/Mesh/nx',
                                '/params/Mesh/ny',
                                '/params/Mesh/qxMax',
                                '/params/Mesh/qxMin',
                                '/params/Mesh/qyMax',
                                '/params/Mesh/qyMin',
                                '/params/Mesh/sliceMax',
                                '/params/Mesh/sliceMin',
                                '/params/Mesh/xMax',
                                '/params/xMin',
                                '/params/yMax',
                                '/params/yMin',
                                '/params/zCoord',
                                '/params/beamline/printout',
                                '/params/Rx',
                                '/params/Ry',
                                '/params/dRx',
                                '/params/dRy',
                                '/params/nval',
                                '/params/photonEnergy',
                                '/params/wDomain',
                                '/params/wEFieldUnit',
                                '/params/wFloatType',
                                '/params/wSpace',
                                '/params/xCentre',
                                '/params/yCentre',
                                '/info/package_version',
                                '/info/contact',
                                '/info/data_description',
                                '/info/method_description',
                                '/misc/xFWHM',
                                '/misc/yFWHM',
                                '/version',
                                ]


    def expectedData(self):
        """ Query for the data expected by the Interactor. """
        return self.__expected_data

    def providedData(self):
        """ Query for the data provided by the Interactor. """
        return self.__provided_data

    def backengine(self):
        """ This method drives the backengine code."""

        # Setup the working directory.
        self._setupWorkingDirectory()

        # Setup path to executable.
        self.path_to_executable = find_executable('feff85L')

        # Copy executable.
        shutil.copy2(self.path_to_executable, self.working_directory)

        # Write parameter deck.
        with open( os.path.join( self.working_directory, 'feff.inp'), 'w' ) as deck:
            self.parameters._serialize( deck )
            deck.close()

        # Execute the code.
        try:
            old_wd = os.getcwd()
            os.chdir( self.working_directory)
            command_line = 'feff85L'
            proc = subprocess.Popen( command_line, shell=True)
            proc.wait()

            # Return.

            os.chdir( old_wd )

        except:
            os.chdir( old_wd )
            return 1

        # Setup data object. This will be a h5py File object residing purely in memory until closed,
        # at which moment it will be written to disk.
        self.__data = h5py.File(self.output_path, driver='core', backing_store=True, mode='w' )

        # Read raw data files.
        atoms = numpy.loadtxt( os.path.join( self.working_directory, 'atoms.dat'), skiprows=2)
        xmu = numpy.loadtxt( os.path.join( self.working_directory, 'xmu.dat'), comments='#')
        chi = numpy.loadtxt( os.path.join( self.working_directory, 'chi.dat'), comments='#', usecols=(2,3))

        # Setup tree and write data on the fly.
        self.__data.create_dataset('data/snp_0000001/r', data=atoms[:,:3])
        #self.__data.create_dataset('data/snp_0000001/xyz', data=None)
        #self.__data.create_dataset('data/snp_0000001/Z', data=None)
        #self.__data.create_dataset('data/snp_0000001/T', data=None)
        self.__data.create_dataset('data/snp_0000001/E', data=xmu[:,0])
        self.__data.create_dataset('data/snp_0000001/DeltaE', data=xmu[:,1])
        self.__data.create_dataset('data/snp_0000001/k', data=xmu[:,2])
        self.__data.create_dataset('data/snp_0000001/mu', data=xmu[:,3])
        self.__data.create_dataset('data/snp_0000001/mu0', data=xmu[:,4])
        self.__data.create_dataset('data/snp_0000001/chi', data=xmu[:,5])
        self.__data.create_dataset('data/snp_0000001/ampl', data=chi[:,0])
        self.__data.create_dataset('data/snp_0000001/phase', data=chi[:,1])
        self.__data.create_dataset('data/snp_0000001/potential_index', data=atoms[:,3])

        self.__data['data/snp_0000001/r'].attrs['unit'] = 'Angstrom'
        self.__data['data/snp_0000001/DeltaE'].attrs['unit'] = 'eV'
        self.__data['data/snp_0000001/E'].attrs['unit'] = 'eV'
        self.__data['data/snp_0000001/k'].attrs['unit'] = '1'
        self.__data['data/snp_0000001/mu'].attrs['unit'] = '1/Angstrom'
        self.__data['data/snp_0000001/mu0'].attrs['unit'] = '1/Angstrom'
        self.__data['data/snp_0000001/chi'].attrs['unit'] = '1'
        self.__data['data/snp_0000001/ampl'].attrs['unit'] = '1'
        self.__data['data/snp_0000001/phase'].attrs['unit'] = 'rad'
        self.__data['data/snp_0000001/potential_index'].attrs['unit'] = '1'
        #self.__data.create_dataset('misc/polarization_tensor', data=None)
        #self.__data.create_dataset('misc/evec', data=None)
        #self.__data.create_dataset('misc/xivec', data=None)
        #self.__data.create_dataset('misc/spvec', data=None)
        #self.__data.create_dataset('misc/nabs', data=None)
        #self.__data.create_dataset('misc/iphabs', data=None)
        #self.__data.create_dataset('misc/cf_average_data', data=None)
        #self.__data.create_dataset('misc/ipol', data=None)
        #self.__data.create_dataset('misc/ispin', data=None)
        #self.__data.create_dataset('misc/le2', data=None)
        #self.__data.create_dataset('misc/elpty', data=None)
        #self.__data.create_dataset('misc/angks', data=None)

        return 0

    @property
    def data(self):
        """ Query for the field data. """
        return self.__data

    @property
    def working_directory(self):
        """ Query the working directory """
        return self.__working_directory
    @working_directory.setter
    def working_directory(self, value):
        """ Set the working directory to a value. """
        if not isinstance( value, str ):
            raise TypeError( "working_directory must be a string (path)." )

        if not os.path.isdir( value ):
            raise RuntimeError( "working_directory must be an existing directory (or link).")

        # All sane, set attribute.
        self.__working_directory = value

    @property
    def path_to_executable(self):
        """ Query the path to the feff executable. """
        return self.__path_to_executable
    @path_to_executable.setter
    def path_to_executable(self, value):
        """ Set the path_to_executable to a value. """
        # Check type.
        if not isinstance( value, str ):
            raise TypeError( "path_to_executable must be a string (path)." )
        # Check is file.
        if not os.path.isfile( value ):
            raise RuntimeError( "path_to_executable must be an existing file (or link).")
        # Check is executable.
        if not stat.S_IXUSR & os.stat(value)[stat.ST_MODE]:
            raise RuntimeError( "path_to_executable must be executable by the user.")

        # All sane, set attribute.
        self.__path_to_executable = value

    def _readH5(self):
        """ """
        """ Private method for reading the hdf5 input and extracting the parameters and data relevant to initialize the object. """
        pass # Nothing to be done since IO happens in backengine.

    def saveH5(self):
        """ """
        """
        Private method to save the object to a file.

        :param output_path: The file where to save the object's data. Default: self.output_path
        :type output_path: str
        """

        # Get the handle to the data.
        data = self.__data
        data.create_dataset('info/contact', data='Carsten Fortmann-Grote <carsten.grote@xfel.eu>')
        data.create_dataset('info/data_description', data='Absorption spectrum and associated data.')
        data.create_dataset('info/interface_version', data='1.0')
        data.create_dataset('info/credits', data='J. J. Rehr et al, "Ab initio theory and calculations of X-ray spectra", Comptes Rendus Physique _10_, 548 (2009). DOI: dx.doi.org/10.1016/j.crhy.2008.08.004')
        data.create_dataset('info/package_version', data='FEFF8.5L')

        data.create_dataset('params/edge', data=self.parameters.edge)
        data.create_dataset('params/amplitude_reduction_factor', data=self.parameters.amplitude_reduction_factor)
        data.create_dataset('params/effective_path_distance', data=self.parameters.effective_path_distance)
        data['params/amplitude_reduction_factor'].attrs['unit'] = '1'
        data['params/edge'].attrs['unit'] = ''
        data['params/effective_path_distance'].attrs['unit'] = 'Angstrom'

        # Close the dataset, this writes the data to disk.
        data.close()

    def _setupWorkingDirectory(self):
        """ Create a temporary directory where to execute the calculation. """

        self.working_directory = tempfile.mkdtemp(prefix='tmp_feff')

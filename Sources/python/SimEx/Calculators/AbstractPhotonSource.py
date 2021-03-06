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

""" Module for AbstractPhotonSource

    @author : CFG
    @institution : XFEL
    @creation 20151007

"""

from abc import ABCMeta
from abc import abstractmethod

from SimEx.Calculators.AbstractBaseCalculator import AbstractBaseCalculator
from SimEx.Utilities.EntityChecks import checkAndSetInstance


class AbstractPhotonSource(AbstractBaseCalculator):
    """
    Class representing an abstract photon source, serving as API for actual photon source simulation calculators.
    """

    # Make this an abstract base class.
    __metaclass__  = ABCMeta

    # Abstract constructor.
    @abstractmethod
    def __init__(self, parameters=None, input_path=None, output_path=None):
        """
        Constructor for the Abstract Photon Source.
        """

        # Check input path. Raises if none given.
        input_path = checkAndSetInstance(str, input_path, None)

        # Check output path. Set default if none given.
        output_path = checkAndSetInstance(str, output_path, 'source_out.h5')

        # Init base class.
        super(AbstractPhotonSource, self).__init__(parameters, input_path, output_path)

        # Setup provided data groups and sets.
        self.__provided_data = ['/data/arrEhor',
                                '/data/arrEver',
                                '/params/Mesh/nSlices',
                                '/params/Mesh/nx',
                                '/params/Mesh/ny',
                                '/params/Mesh/sliceMax',
                                '/params/Mesh/sliceMin',
                                '/params/Mesh/xMax',
                                '/params/Mesh/xMin',
                                '/params/Mesh/yMax',
                                '/params/Mesh/yMin',
                                '/params/Mesh/zCoord',
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
                                '/history/parent/info/data_description',
                                '/history/parent/info/package_version',
                                '/history/parent/misc/FAST2XY.DAT',
                                '/history/parent/misc/angular_distribution',
                                '/history/parent/misc/spot_size',
                                '/history/parent/misc/gain_curve',
                                '/history/parent/misc/nzc',
                                '/history/parent/misc/temporal_struct',
                                '/version',
                                ]

        # Setup expected data.
        self.__expected_data = [d for d in self.__provided_data]

    def expectedData(self):
        """
        Return the list of expected data sets with full paths.

        @return : List of strings, e.g. [/data/data1, /params/params1']
        """
        return self.__expected_data

    def providedData(self):
        """
        Return the list of provided data sets with full paths.

        @return : List of strings, e.g. [/data/data1, /params/params1']
        """
        return self.__provided_data


def checkAndSetPhotonSource(var=None, default=None):
    """
    Check if passed object is an AbstractPhotonSource instance. If non is given, set to given default.

    @param var : The object to check.
    @param default : The default to use.
    @return : The checked photon source object.
    @throw : RuntimeError if no valid PhotonSource was given.
    """

    return checkAndSetInstance(AbstractPhotonSource, var, default)


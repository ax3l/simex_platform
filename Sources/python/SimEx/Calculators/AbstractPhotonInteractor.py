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

""" Module for AbstractPhotonInteractor

    @author : CFG
    @institution : XFEL
    @creation 20151007

"""

from abc import ABCMeta
from abc import abstractmethod

from SimEx.Calculators.AbstractBaseCalculator import AbstractBaseCalculator
from SimEx.Utilities.EntityChecks import checkAndSetInstance


class AbstractPhotonInteractor(AbstractBaseCalculator):
    """
    Class representing an abstract photon source, serving as API for actual photon source simulation calculators.
    """

    __metaclass__  = ABCMeta
    @abstractmethod
    def __init__(self, parameters=None, input_path=None, output_path=None):
        #"""
        #Constructor for the Abstract Photon Interactor.
        #"""
        super(AbstractPhotonInteractor, self).__init__(parameters, input_path, output_path)

def checkAndSetPhotonInteractor(var=None, default=None):
    """
    Check if passed object is an AbstractPhotonInteractor instance. If non is given, set to given default.

    @param var : The object to check.
    @param default : The default to use.
    @return : The checked photon source object.
    @throw : RuntimeError if no valid PhotonInteractor was given.
    """

    return checkAndSetInstance(AbstractPhotonInteractor, var, default)


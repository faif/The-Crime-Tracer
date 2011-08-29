# -*- coding: utf-8 -*-

#    Class Exceptions.
#
#    This file is part of The Crime Tracer.
#
#    Copyright (C) 2009-11 Free Software Gaming Geeks <fsgamedev@googlegroups.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


## @package class_exceptions
#  Game's Class Exceptions.
#
# This module contains all class exceptions used in the game.


## base class for all exceptions.
#
class Error(Exception):
    pass


## class for a specific exception.
#
class SpecificException(Error):

    ## the constructor of the exception
    #
    # @param self the object pointer
    # @param value informative exception value
    def __init__(self, value):
        ## informative exception value
        self.value = value

    ## the string representation of the exception
    #
    # @param self the object pointer
    def __str__(self):
        return repr(self.value)

# test the script if executed
if __name__ == '__main__':
    import sys
    print((' '.join(('Testing', sys.argv[0]))))
    try:
        raise SpecificException(2*2)
    except SpecificException as e:
        print((' '.join(('Exception occurred, value', str(e)))))

# -*- coding: utf-8 -*-

#    Generic object-oriented utilities.
#
#    This file is part of The Crime Tracer.
#
#    Copyright (C) 2010-11 Free Software Gaming Geeks <fsgamedev@googlegroups.com>
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


## @package base
#  Generic object-oriented utilities.
#
# This module contains object-oriented stuff that are generic enough
# to be useful in more than one (sub)classes. 

## objects imported when `from <module> import *' is used
__all__ = ['Base']


## a base class
#
class Base(object):

    ## print all the attributes of an object
    #
    # @param self the object pointer
    def print_attrs(self):
        for attr in self.__dict__:
            print(attr, getattr(self, attr))

    ## find in which class the method of a
    ## specific instance belongs
    #
    # @param self the object pointer
    # @param method the method's name as a plain string
    def find_class(self, method):
        for ty in type(self).mro():
            if method in ty.__dict__:
                return ty

# test the script if executed
if __name__ == '__main__':
    import sys
    print((' '.join(('Testing', sys.argv[0]))))
    b = Base()
    print(b.find_class('print_attrs'))

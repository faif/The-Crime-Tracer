# -*- coding: utf-8 -*-

#    Functions useful for debugging.
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

'''Debugging functions.

This module contains functions that can print/return useful debugging
information.
'''

__all__ = ['Debug']

class Debug:

    def print_attrs(self):
        '''print all the attributes of an object'''
        for attr in self.__dict__:
            print(attr, getattr(self, attr))

    def find_class(self, method):
        '''find in which class the method of a specific instance belongs'''
        for ty in type(self).mro():
            if method in ty.__dict__:
                return ty

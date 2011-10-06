#  -*- coding: utf-8 -*-

#    Borg (Design Pattern) Class Implementation.
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

'''Borg Debisn Pattern.

Implementation of the Borg Design Pattern that it is used for sharing the
same state between different objects.
'''

__all__ = [ 'Borg' ]

class Borg(object):
    '''The simplest Borg Implementation.'''
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state

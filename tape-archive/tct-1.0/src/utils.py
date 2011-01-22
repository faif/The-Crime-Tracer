# -*- coding: utf-8 -*-

#    Generic Utilities.
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


## @package utils
#  Generic Utilities.
#
# This module contains some utilities which support
# various generic operations (type conversions, etc.).

## objects imported when `from <module> import *' is used
__all__ = ['get_time_sec']


## get the clock's time in seconds
#
# @param time_passed the clock's time
# @return the clock's time in seconds
def get_time_sec(time_passed):
    assert(time_passed > 0.0)
    time_sec = time_passed / 1000.0
    return time_sec

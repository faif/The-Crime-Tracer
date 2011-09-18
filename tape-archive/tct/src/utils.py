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


'''Generic Utilities.

This module contains utilities that can be used for tracking time, etc.
'''

__all__ = ['get_time_sec']

def get_time_sec(time_passed):
    # TODO: unit test instead of assertion
    assert(time_passed > 0.0)
    time_sec = time_passed / 1000.0
    return time_sec

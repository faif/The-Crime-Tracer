# -*- coding: utf-8 -*-

#    Operating System Utilities.
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


## @package os_utils
#  Operating System Utilities.
#
# This module contains some utilities which support
# operating system operations (locating files, etc).


try:
    import constants
    from pygame import quit
    from os import path
except ImportError as err:
    try:
        import os
        path = os.path.basename(__file__)
        print((': '.join((path, str(err)))))
    # importing os failed, print a custom message...
    except ImportError:
        print((': '.join(("couldn't load module", str(err)))))
    exit(2)

## objects imported when `from <module> import *' is used
__all__ = ['file_path', 'safe_exit']


## create the path of a file
#
# @param filename the name of the file
# @param dir the parent directory of the file
# @return the path of the file
def file_path(filename, dir):
    fullname = path.join(constants.RESOURCES_DIR, dir)
    fullname = path.join(fullname, filename)
    return fullname


## perform safe exit operation
#
def safe_exit():
    # windows needs to close pygame's
    # subsystems first, before exit
    quit()

    # now exit succesfully
    exit()

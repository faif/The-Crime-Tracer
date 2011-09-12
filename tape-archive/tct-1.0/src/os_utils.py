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


'''Operating System Utilities.

This module contains some utilities which support
operating system operations (locating files, etc).
'''

try:
    import constants
    from pygame import quit
    from os import path
except (RuntimeError, ImportError) as err:
        import os
        from constants import MOD_FAIL_ERR
        path = os.path.basename(__file__)
        print('{0}: {1}'.format(path, err))
        exit(MOD_FAIL_ERR)

__all__ = ['file_path', 'safe_exit']


def file_path(filename, dir):
    fullname = path.join(constants.RESOURCES_DIR, dir)
    fullname = path.join(fullname, filename)
    return fullname

def safe_exit():
    # windows needs to close pygame's
    # subsystems first, before exit
    quit()

    # now exit succesfully
    exit()

# -*- coding: utf-8 -*-
#
#    Command Line Options Parser.
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

'''Command Line Options Parser.

This module contains functions which parse the command
line options of the game and initialize the flag variables.
'''

try:
    import argparse
    import constants
    from time import strftime, gmtime
except (RuntimeError, ImportError) as err:
        import os
        from constants import MOD_FAIL_ERR
        path = os.path.basename(__file__)
        print('{0}: {1}'.format(path, err))
        exit(MOD_FAIL_ERR)

YEAR_FULL = strftime('%Y', gmtime())
YEAR_ABBR = strftime('%y', gmtime())
EPILOGUE = 'Report bugs to fsgamedev@googlegroups.com'
PROGRAM = 'tct.py'
USAGE = '%(prog)s [OPTIONS]'
DESC = 'Available command line options for %(prog)s'

LICENSE = (
  'Copyright (C) 2009-{0} Free Software Gaming Geeks <fsgamedev@googlegroups.com>'.format(YEAR_ABBR),
  '',
  'This program is free software: you can redistribute it and/or modify',
  'it under the terms of the GNU General Public License as published by',
  'the Free Software Foundation, either version 3 of the License, or',
  '(at your option) any later version.',
  '',
  'This program is distributed in the hope that it will be useful,',
  'but WITHOUT ANY WARRANTY; without even the implied warranty of',
  'MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the',
  'GNU General Public License for more details.',
  '',
  'You should have received a copy of the GNU General Public License',
  'along with this program.  If not, see <http://www.gnu.org/licenses/>.'
)

VERSION = (
    '{0}'.format(constants.GAME_PACKAGE),
    'Copyright (C) {0} Free Software Gaming Geeks.'.format(YEAR_FULL),
    'License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.',
    'This is free software: you are free to change and redistribute it.',
    'There is NO WARRANTY, to the extent permitted by law.',
    '',
    'Written by Sakis Kasampalis and Efstathios Xatzikiriakidis.',
)

class VersionAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        for line in VERSION:
            print(line)

class CopyrightAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        for line in LICENSE:
            print(line)

def get_parsed_opts():
    '''create a parser and return the namespace with the parsed options'''
    parser = argparse.ArgumentParser(prog=PROGRAM, description=DESC,
                                     epilog=EPILOGUE, usage=USAGE)

    group = parser.add_argument_group('game control arguments')
    group.add_argument('-f, --fullscreen', default=False, dest='fullscreen',
                   action='store_true', help='run in fullscreen mode')
    group.add_argument('--nomusic', default=True, dest='music',
                   action='store_false', help='disable audio themes')
    group.add_argument('--nosound', default=True, dest='sound',
                   action='store_false', help='disable audio clips')

    group = parser.add_argument_group('game info arguments')
    group.add_argument('--version', action=VersionAction, nargs=0,
                       help='print version information')
    group.add_argument('-c, --copyright', action=CopyrightAction, nargs=0,
                        help='print copyright information')

    group = parser.add_argument_group('debugging arguments')
    group.add_argument('-v, --verbose', default=False, dest='verbose',
                        action='store_true', help='explain what is going on')

    args = parser.parse_args()

    return args

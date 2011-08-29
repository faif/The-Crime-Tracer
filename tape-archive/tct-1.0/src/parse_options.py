# -*- coding: utf-8 -*-

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
line options of the game and initialize flag variables.
'''

try:
    import constants
    from optparse import OptionParser, OptionGroup
except Exception as err:
        import constants, os
        path = os.path.basename(__file__)
        print('{0}: {1}'.format(path, err))
        exit(MOD_FAIL_ERR)

__all__ = ['get_parsed_opts']

def show_gnu_gpl(option, opt, value, parser):
    for line in constants.GAME_GPL:
        print(line)
    exit()

def show_authors(option, opt, value, parser):
    for line in constants.GAME_AUTHORS:
        print(line)
    exit()

def get_parsed_opts():
    usage = "Usage: %prog [OPTIONS]"

    parser = OptionParser(usage=usage, version=constants.GAME_PACKAGE)

    group = OptionGroup(parser, "Info Options")

    group.add_option("-a", "--author",
                     action="callback", callback=show_authors,
                     help="print the authors of the game")

    group.add_option("-c", "--copyleft",
                     action="callback", callback=show_gnu_gpl,
                     help="print the short version of GNU GPL")

    group.add_option("-l", "--license",
                     action="callback", callback=show_gnu_gpl,
                     help="works like `-c' and `--copyleft'")

    parser.add_option_group(group)

    group = OptionGroup(parser, "Game Options")

    group.add_option("-f", "--fullscreen", default=False,
                     action="store_true", dest="fullscreen",
                     help="run in fullscreen mode")

    group.add_option("--nomusic", default=True,
                     dest="music", action="store_false",
                     help="disable sounds")

    group.add_option("--nosound", action="store_false",
                     dest="sound", default=True,
                     help="disable music")

    parser.add_option_group(group)

    group = OptionGroup(parser, "Debug Options")

    group.add_option("-v", "--verbose", default=False,
                     action="store_true", dest="verbose",
                     help="explain what is being done")

    parser.add_option_group(group)

    options, arguments = parser.parse_args()

    if arguments:
        parser.error("invalid argument")

    return options

# -*- coding: utf-8 -*-

#    Game's Command Line Options Parser.
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


## @package parse_options
#  Command Line Options Parser.
#
# This module contains functions which parse the command
# line options of the game and initialize flag variables.


try:
    import constants
    from optparse import OptionParser, OptionGroup
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
__all__ = ['get_parsed_opts']


## show the GNU GPL license and exit normally
#
# @param option the option instance that's calling the callback
# @param opt the option string seen on the command line
# @param value the argument to this option seen on the command line
# @param parser the OptionParser instance driving the whole thing
def show_gnu_gpl(option, opt, value, parser):
    # print license
    for line in constants.GAME_GPL:
        print(line)

    # and exit
    exit()


## show the authors of the game and exit normally
#
# @param option the option instance that's calling the callback
# @param opt the option string seen on the command line
# @param value the argument to this option seen on the command line
# @param parser the OptionParser instance driving the whole thing
def show_authors(option, opt, value, parser):
    # print authors
    for line in constants.GAME_AUTHORS:
        print(line)

    # and exit
    exit()


## parse and return the game's command line options
#
# @return the game's options' flags
def get_parsed_opts():
    # the usage info of the game
    usage = "Usage: %prog [OPTIONS]"

    # create an option parser object and pass to it basic info
    parser = OptionParser(usage=usage, version=constants.GAME_PACKAGE)

    # add the options and their behavior of the game

    # create info options group
    group = OptionGroup(parser, "Info Options")

    # add to the group the options
    group.add_option("-a", "--author",
                     action="callback", callback=show_authors,
                     help="print the authors of the game")

    group.add_option("-c", "--copyleft",
                     action="callback", callback=show_gnu_gpl,
                     help="print the short version of GNU GPL")

    group.add_option("-l", "--license",
                     action="callback", callback=show_gnu_gpl,
                     help="works like `-c' and `--copyleft'")

    # add the group to the parser
    parser.add_option_group(group)

    # create game options group
    group = OptionGroup(parser, "Game Options")

    # add to the group the options
    group.add_option("-f", "--fullscreen", default=False,
                     action="store_true", dest="fullscreen",
                     help="run in fullscreen mode")

    group.add_option("--nomusic", default=True,
                     dest="music", action="store_false",
                     help="disable sounds")

    group.add_option("--nosound", action="store_false",
                     dest="sound", default=True,
                     help="disable music")

    # add the group to the parser
    parser.add_option_group(group)

    # create debug options group
    group = OptionGroup(parser, "Debug Options")

    # add to the group the options
    group.add_option("-v", "--verbose", default=False,
                     action="store_true", dest="verbose",
                     help="explain what is being done")

    # add the group to the parser
    parser.add_option_group(group)

    # parse the command line options of the game
    options, arguments = parser.parse_args()

    # if there are arguments terminate the game
    if arguments:
        parser.error("invalid argument")

    # return the flag options to the caller
    return options


# test the script if executed
if __name__ == '__main__':
    import sys
    print((' '.join(('Testing', sys.argv[0]))))
    get_parsed_opts()

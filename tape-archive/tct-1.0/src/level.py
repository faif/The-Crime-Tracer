# -*- coding: utf-8 -*-

#    Experimenting with level design and creation
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


try:
    import constants
    from base import Base
    from fsm import State
    from os_utils import safe_exit
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
__all__ = ['LevelFactory']

## the "right" way to create a new level (exposed interface)
#
class LevelFactory(Base):

    ## create a new level
    #
    # @param self the object pointer
    # @param name the level's name
    def create_level(self, name, game_opts):
        # find out which factory to use
        if (name == constants.SCENES['level_one']):
            self.factory = LevelOne(game_opts)
        else:
            raise ValueError('No such level', name)

        # build the actual level
        lev =  self.factory.create_level()
        assert(lev is not None)
        # return the object instance to the game manager
        return self.factory


## one factory for each level because there might be
## differences (different number and type of rooms, etc)
#
class LevelOne(State):
    # part of the borg pattern
    __shared_state = {}

    def __init__(self, game_opts):
        # part of the borg pattern
        self.__dict__ = self.__shared_state

        # initialize the state
        State.__init__(self, constants.SCENES['level_one'])
        self.game_opts = game_opts

    # rooms, doors, obstacles, etc.
    def create_level(self):
        print('creating level 1')
        r1 = self.create_room('office')
        r2 = self.create_room('park')
        lev = (r1, r2)
        return lev
        
    def create_room(self, name):
        return Room(name)

    def create_door(self, colour):
        return Door(colour)

    ## what to do when the level is enabled
    #
    # @param self the object pointer
    def do_actions(self):
        print('exiting...')
        safe_exit()

## not necessary but makes inheritance more clear
#
class MapSite: pass

class Room(MapSite):
    def __init__(self, name):
        self.name = name

    def enter(self):
        print('entering a room')

class Door(MapSite):
    def __init__(self, colour):
        self.colour = colour

    def enter(self):
        print('entering a door')

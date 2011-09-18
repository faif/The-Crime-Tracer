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
    from fsm import FSM, State
    from os_utils import safe_exit
except (RuntimeError, ImportError) as err:
        import os
        from constants import MOD_FAIL_ERR
        path = os.path.basename(__file__)
        print('{0}: {1}'.format(path, err))
        exit(MOD_FAIL_ERR)

__all__ = ['LevelFactory']


class LevelFactory(Base):
    def create_level(self, name):
        # find out which factory to use
        if (name == constants.SCENES['level_one']):
            self.factory = LevelOneFactory()
        else:
            raise ValueError('No such level', name)

        # build the actual level
        lev =  self.factory.create_level()

        # return the object instance to the game manager
        return self.factory


class LevelOneFactory(State):
    '''One factory for each level because there might be
    differences (different number and type of rooms, etc)
    '''
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state
        State.__init__(self, constants.SCENES['level_one'])
        self.states = FSM()
        self.states.active_state = None

    # rooms, doors, obstacles, etc.
    def create_level(self):
        print('creating level 1')

        # set and group the rooms
        r1 = self.create_room('office')
        r2 = self.create_room('park')
        level = (r1, r2)

        # add the rooms to the state machine
        for r in level:
            self.states.add_state(r)

        # enable the default state
        self.states.active_state = level[0]

        return self.states

    def run(self):
        self.states.run()
        
    def create_room(self, name):
        return Room(name)

    def create_door(self, colour):
        return Door(colour)

    def do_actions(self):
        safe_exit()


class MapSite: pass

class Room(State):
    def __init__(self, name):
        self.name = name
        State.__init__(self, self.name)

    def do_actions(self):
        print('Your are in the', str(self))

    def __str__(self):
        return self.name

    def enter(self):
        print('entering', str(self))

class Door(MapSite):
    def __init__(self, colour):
        self.colour = colour
        self.open = False

    def open(self):
        print('opening door')

class Item(MapSite):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def pick(self):
        print('picking', str(self))

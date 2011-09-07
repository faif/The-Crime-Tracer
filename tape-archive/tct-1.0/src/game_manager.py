# -*- coding: utf-8 -*-

#    Game Manager.
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


'''The Game Manager.

This module contains the game manager which keeps
track of the active scene (i.e. intro, menu, level 1,
etc.), switches between scenes, etc.
'''

try:
    import constants
    from fsm import FSM
    from intro import Intro
    from menu import Menu
    from borg import Borg
    from base import Base
    from level import LevelFactory
except (RuntimeError, ImportError) as err:
        import os
        from constants import MOD_FAIL_ERR
        path = os.path.basename(__file__)
        print('{0}: {1}'.format(path, err))
        exit(MOD_FAIL_ERR)

__all__ = ['GameManager']

class GameManager(Borg):
    '''The game manager class is responsible for keeping
    track of the active scene (i.e. intro, menu, level 1, 
    etc), changing between scenes, etc.'''

    def __init__(self, game_opts):
        super(GameManager, self).__init__()

        self.scenes = FSM()

        # TODO: find a way of applying lazy initialisation
        # on level creation - a level should be created only
        # right before executed
        # flev = LevelFactory().create_level(
        #     constants.SCENES['level_one'],
        #     game_opts)
        flev = LevelFactory().create_level(
            constants.SCENES['level_one']
            )

        # set and group the scenes
        scenes = (Intro(game_opts), Menu(game_opts), 
                  flev)

        # add the scenes to the state machine
        for s in scenes:
            self.scenes.add_state(s)
        
        # enable the default state
        self.scenes.active_state = scenes[0]

    def run_scene(self):
        '''execute the appropriate scene'''
        self.scenes.run()

    def set_active_scene(self, scene):
        '''switch the active scene and start the new one'''
        self.scenes.set_state(scene)
        self.run_scene()

    def __str__(self):
        return '{0} executes {1}'.format(self.__class__.__name__,
                                         self.scenes.active_state)

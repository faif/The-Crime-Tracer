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


## @package game_manager
#  The Game Manager.
#
# This module contains the game manager which keeps
# track of the active scene (i.e. intro, menu, level 1,
# etc.), switches between scenes, etc.


try:
    import constants
    from fsm import FSM
    from intro import Intro
    from menu import Menu
    from base import Base
    from level import LevelFactory
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
__all__ = ['GameManager']


## a game manager class
#
# The game manager is responsible for keeping
# track of the active scene (i.e. intro, menu,
# level 1, etc), changing between scenes, etc.
# It's a borg since we need a shared state for
# all instances.
class GameManager(Base):
    # part of the borg pattern
    __shared_state = {}

    ## initialize the game manager
    #
    # @param self the object pointer
    # @param game_opts the game's command line options
    def __init__(self, game_opts):
        # part of the borg pattern
        self.__dict__ = self.__shared_state

        ## the game scenes/levels
        self.scenes = FSM()

        # initialise a sample level
        # TODO: find a way of applying lazy initialisation
        # on level creation - a level should be created only
        # right before executed
        flev = LevelFactory().create_level(
            constants.SCENES['level_one'],
            game_opts)

        # set and group the scenes
        scenes = (Intro(game_opts), Menu(game_opts), 
                  flev)

        # add the scenes to the state machine
        for s in scenes:
            self.scenes.add_state(s)
        
        # enable the default state
        self.scenes.active_state = scenes[0]

    ## execute the appropriate scene
    #
    # @param self the object pointer
    def run_scene(self):
        self.scenes.run()

    ## switch the active scene and start the new one
    #
    # @param self the object pointer
    # @param scene the name of the new active scene
    def set_active_scene(self, scene):
        self.scenes.set_state(scene)
        self.run_scene()


    ## the string representation of the game manager
    #
    # @param self the object pointer
    # @return a string which shows which state is executed
    def __str__(self):
        return ' '.join((self.__class__.__name__, 
                        'executes',
                        str(self.scenes.active_state)))


# test the script if executed
if __name__ == '__main__':
    import sys
    print((' '.join(('Testing', sys.argv[0]))))
    # comment the constructor except from the 1st
    # line and uncomment the code below to test
    # if borg works as expected
    # g = GameManager(None)
    # g.x = 3
    # g2 = GameManager(None)
    # g2.x = 5
    # print((g.x, g2.x))

# -*- coding: utf-8 -*-

#    Intro Screen.
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


## @package intro
#  Intro Screen.
#
# This module contains the game's intro screen implementation.


try:
    import constants, pygame, sound_mixer, graphics
    from intro_cut_scene import IntroCutScene
    from fsm import State
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
__all__ = ['Intro']

MAX_VOLUME = 1.0


## class for game's intro screen
#
class Intro(State):

    ## initialize the intro screen
    #
    # @param self the object pointer
    # @param game_opts the game's command line options
    def __init__(self, game_opts):
        # initialize the state
        State.__init__(self, constants.SCENES['intro'])

        ## the game's command line options
        self.game_opts = game_opts

        ## intro slides
        slide_num = len(constants.FILES['graphics']['intro']['slides'])
        self.slides = [
            graphics.load_image(
                constants.FILES['graphics']['intro']
                ['slides'][i])[0] for i in range(slide_num)
            ]

        ## cut scenes object
        self.cutscenes = IntroCutScene(self.slides)

        # set sound volume to minimum
        pygame.mixer.music.set_volume(0.0)

        # play the background music theme
        sound_mixer.play_music(
            constants.FILES['sounds']['menu']['share']['bg'][0])

        # pause or unpause music according to user preference
        if self.game_opts.music:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

        # set sound volume to maximum
        pygame.mixer.music.set_volume(MAX_VOLUME)

    ## what to do when the intro is enabled
    #
    # @param self the object pointer
    def do_actions(self):
        # run the intro slideshow
        self.cutscenes.run()

    ## what should be satisfied for enabling the next scene
    #
    # @param self the object pointer        
    # @return the name of the next scene        
    def check_conditions(self):
        # if the scene is finished, returns back
        # to the caller the name of the next one
        if self.cutscenes.controller.is_finished:
            return constants.SCENES['menu']
        return None

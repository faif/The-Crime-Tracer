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

'''Intro Screen.

This module contains the game's intro screen implementation.
'''

try:
    import constants, pygame, sound_mixer, graphics
    from intro_cut_scene import IntroCutScene
    from fsm import State
except (RuntimeError, ImportError) as err:
        import os
        from constants import MOD_FAIL_ERR
        path = os.path.basename(__file__)
        print('{0}: {1}'.format(path, err))
        exit(MOD_FAIL_ERR)

__all__ = ['Intro']

MAX_VOLUME = 1.0

class Intro(State):

    def __init__(self, game_opts):
        State.__init__(self, constants.SCENES['intro'])
        self.game_opts = game_opts

        # intro slides
        slide_num = len(constants.FILES['graphics']['intro']['slides'])
        self.slides = [
            graphics.load_image(
                constants.FILES['graphics']['intro']
                ['slides'][i])[0] for i in range(slide_num)
            ]
        self.cutscenes = IntroCutScene(self.slides)

        pygame.mixer.music.set_volume(0.0)
        sound_mixer.play_music(
            constants.FILES['sounds']['menu']['share']['bg'][0])
        if self.game_opts.music:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
        pygame.mixer.music.set_volume(MAX_VOLUME)

    def do_actions(self):
        # run the intro slideshow
        self.cutscenes.run()

    def check_conditions(self):
        # if the scene is finished, return back
        # to the caller the name of the next one
        if self.cutscenes.controller.is_finished:
            return constants.SCENES['menu']
        return None

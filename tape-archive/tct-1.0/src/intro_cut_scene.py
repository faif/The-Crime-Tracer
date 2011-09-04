# -*- coding: utf-8 -*-

#    Intro Slides Implementation.
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


'''Intro Cut Scene Implementation.

This module contains the intro slides implementation.
'''

try:
    import constants, pygame, graphics
    from pygame.locals import *
    from os_utils import safe_exit
    from base import Base
    from mvc import SafeExitEvent, EventManager, EscapeEvent, ReturnEvent
except (RuntimeError, ImportError) as err:
        import os
        from constants import MOD_FAIL_ERR
        path = os.path.basename(__file__)
        print('{0}: {1}'.format(path, err))
        exit(MOD_FAIL_ERR)

__all__ = ['IntroCutScene']

SLIDE_CLOCK_TICK = 80
SLIDE_ALPHA_FADE = 5
MAX_ALPHA = 255
SLIDE_PRESENCE_DELAY = 100
SLIDE_MONAD_DELAY = 10

class IntroCutSceneController:
    '''This class is responsible for keeping the slides executed until
    they finish (normally or after request), exit the game while the
    slides are active, etc.
    '''
    def __init__(self, manager, view):
        self.event_manager = manager
        self.event_manager.register_listener(self)
        self.gui_view = view
        self.clock = pygame.time.Clock()
        self.is_finished = False
        self.time = SLIDE_PRESENCE_DELAY

    def run(self):
        for slide in self.gui_view.slides:
            evt = None

            self.time = SLIDE_PRESENCE_DELAY

            # exit immediately if the user wants to
            if self.is_finished:
                return

            while self.gui_view.alphavalue >= 0:
                # set the blank slide alternation delay 
                self.clock.tick(SLIDE_CLOCK_TICK)
                self.gui_view.alphavalue -= SLIDE_ALPHA_FADE
                self.gui_view.next_slide(slide)

            # show the slide for some time
            while self.time >= 0:
                # delay for each time monad
                self.clock.tick(SLIDE_MONAD_DELAY)

                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        evt = SafeExitEvent()

                key = pygame.key.get_pressed()
                # the user wants to skip the active slide
                if key[K_RETURN] or key[K_SPACE]:
                    evt = ReturnEvent()
                # the user wants to skip all the slides
                elif key[K_ESCAPE]:
                    evt = EscapeEvent()
                # the user wants to exit the game
                elif key[K_q]:
                    evt = SafeExitEvent()
                
                # inform the event manager about the generated event
                if evt:
                    self.event_manager.post(evt)

                self.time -= 1

            while self.gui_view.alphavalue <= MAX_ALPHA:
                self.clock.tick(SLIDE_CLOCK_TICK)
                self.gui_view.alphavalue += SLIDE_ALPHA_FADE
                self.gui_view.next_slide(slide)

        # the scene is finished normally
        self.is_finished = True

    def notify(self, event):
        # go to the next slide
        if isinstance(event, ReturnEvent):
            self.time = 0
        # skip all the slides
        elif isinstance(event, EscapeEvent):
            self.time = 0
            self.is_finished = True
        # quit the game
        elif isinstance(event, SafeExitEvent):
            safe_exit()

class IntroCutSceneGUIView(Base):
    '''This class is responsible for initialising all the intro cut scene 
    GUI-related stuff and handling the related events.
    '''
    def __init__(self, manager, slides):
        self.event_manager = manager
        self.event_manager.register_listener(self)

        self.screen = pygame.display.get_surface()

        # TODO unit test instead of assertion
        assert(len(slides) > 0)
        self.slides = slides

        self.blank = graphics.load_image(
            constants.FILES['graphics']['intro']['blank'][0])[0].convert()
        self.alphavalue = MAX_ALPHA

    def notify(self, event):
        '''Handle the related events.'''

    def next_slide(self, slide):
        '''Blit the given slide on screen.'''
        self.blank.set_alpha(self.alphavalue)

        # blit the slide
        s = self.screen.blit(slide, (0, 0))
        # blit the blank slide
        bs = self.screen.blit(self.blank, (0, 0))

        # pass only the changes to update
        up_l = (s, bs)
        pygame.display.update(up_l)

class IntroCutScene(Base):
    def __init__(self, slides):
        self.event_manager = EventManager()
        self.gui_view = IntroCutSceneGUIView(self.event_manager, slides)
        self.controller = IntroCutSceneController(self.event_manager, self.gui_view)

    def run(self):
        self.controller.run()

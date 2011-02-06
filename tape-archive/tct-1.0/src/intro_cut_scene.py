# -*- coding: utf-8 -*-

#    Intro Cut Scene Implementation.
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


## @package intro_cut_scene
#  Intro Cut Scene Implementation.
#
# This module contains the game's intro cut scenes implementation.


try:
    import constants, pygame, graphics
    from pygame.locals import *
    from os_utils import safe_exit
    from base import Base
    from mvc import SafeExitEvent, EventManager, KeyboardController, QuitEvent
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
__all__ = ['IntroCutScene']

SLIDE_CLOCK_TICK = 80
SLIDE_ALPHA_FADE = 5
MAX_ALPHA = 255
SLIDE_PRESENCE_DELAY = 100
SLIDE_MONAD_DELAY = 10


## class of the intro cut scene controller
#
# This class is responsible for keeping the cut scenes executed until
# they finish (normally or after request), exit the game while the cut
# scenes are active, etc.
class IntroCutSceneController:
    ## create a new controller and register it as a listener
    #
    # @param self the object pointer
    # @param manager the event manager
    # @param view the view part of MVC
    def __init__(self, manager, view):
        self.event_manager = manager
        self.event_manager.register_listener(self)
        self.gui_view = view

        ## create clock and track time
        self.clock = pygame.time.Clock()

        ## flag to indicate if the scene is finished
        self.is_finished = False


    ## run the slideshow
    #
    # @param self the object pointer
    def run(self):
        # perform cutscene slides main process
        for slide in self.gui_view.slides:
            evt = None

            # exit immediately if the user wants to
            if self.is_finished:
                return

            # while the alpha of the blank slide is not zero
            while self.gui_view.alphavalue >= 0:
                # set the blank slide alternation delay 
                self.clock.tick(SLIDE_CLOCK_TICK)

                # decrease alpha value
                self.gui_view.alphavalue -= SLIDE_ALPHA_FADE

                # show the next slide
                self.gui_view.next_slide(slide)

            # set the slides presence delay 
            time = SLIDE_PRESENCE_DELAY

            # show the slide for some time
            while time >= 0:
                # delay for each time monad
                self.clock.tick(SLIDE_MONAD_DELAY)

                # intro event loop
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        evt = SafeExitEvent()

                # handle keyboard keys
                key = pygame.key.get_pressed()
                # when user presses return key or space key
                if key[K_RETURN] or key[K_SPACE]:
                    # force to go to the next slide
                    time = 0
                # the user wants to skip the introduction
                elif key[K_ESCAPE]:
                    time = 0
                    self.is_finished = True
                # the user wants to exit the game
                elif key[K_q]:
                    evt = SafeExitEvent()
                
                # inform the event manager about the generated event
                if evt:
                    self.event_manager.post(evt)

                # decrease the time where a slide is showed
                time -= 1

            # while the alpha of the blank slide is not zero
            while self.gui_view.alphavalue <= MAX_ALPHA:
                # set the blank slide alternation delay 
                self.clock.tick(SLIDE_CLOCK_TICK)

                # decrease alpha value
                self.gui_view.alphavalue += SLIDE_ALPHA_FADE

                # show the next slide                
                self.gui_view.next_slide(slide)

        # the scene is finished
        self.is_finished = True

    ## handle the related events 
    #
    # @param self the object pointer
    # @param event the generated event
    def notify(self, event):
        if isinstance(event, QuitEvent):
            self.keep_going = False
        elif isinstance(event, SafeExitEvent):
            safe_exit()


## class of the intro cut scenes GUI view
#
# This class is responsible for initialising all the intro cut scene 
# GUI-related stuff and handling the related events
class IntroCutSceneGUIView(Base):
    ## initialize in order to cut scenes
    #
    # @param self the object pointer
    # @param manager the event manager
    # @param slides the list of slides images
    def __init__(self, manager, slides):
        self.event_manager = manager
        self.event_manager.register_listener(self)

        ## the screen surface
        self.screen = pygame.display.get_surface()

        ## the list of background slides
        assert(len(slides) > 0)
        self.slides = slides

        ## the blank background slide
        self.blank = graphics.load_image(
            constants.FILES['graphics']['intro']['blank'][0])[0].convert()
        
        ## set the alpha to maximum value
        self.alphavalue = MAX_ALPHA

    ## handle the related events 
    #
    # @param self the object pointer
    # @param event the generated event
    def notify(self, event):
        pass

    ## blit the given slide on screen
    #
    # @param self the object pointer
    # @param slide the object to blit
    def next_slide(self, slide):
        # set the new alpha value of the blank slide
        self.blank.set_alpha(self.alphavalue)

        # blit the slide
        s = self.screen.blit(slide, (0, 0))

        # blit the blank slide
        bs = self.screen.blit(self.blank, (0, 0))

        # pass only the changes to update
        up_l = (s, bs)

        # display the screen surface
        pygame.display.update(up_l)


## class for game's intro cut scene actions
#
class IntroCutScene(Base):

    ## initialize in order to cut scenes
    #
    # @param self the object pointer
    # @param slides the list of slides images
    def __init__(self, slides):
        self.event_manager = EventManager()
        # TODO use the keyboard controller instead of reimplementing
        # the keyboard functionality inside the cut scene controller
        # self.keyboard_controller = KeyboardController(self.event_manager) 
        self.gui_view = IntroCutSceneGUIView(self.event_manager, slides)
        self.controller = IntroCutSceneController(self.event_manager, self.gui_view)

    ## run the slideshow
    #
    # @param self the object pointer
    def run(self):
        self.controller.run()

# test the script if executed
if __name__ == '__main__':
    import sys
    print((' '.join(('Testing', sys.argv[0]))))

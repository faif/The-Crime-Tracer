#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

#    Main Entry Point.
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

'''Main Entry Point.

This module contains the main entry point. It checks
for any inserted command line options, creates a window
and then starts the game manager for the rest things.
'''

try:
    import os, sys, pygame, constants
    from command_line_parser import get_parsed_opts
    from graphics import load_image
    from game_manager import GameManager
    from base import Base
    from mvc import KeyboardController, EventManager
except (RuntimeError, ImportError) as err:
        import os
        from constants import MOD_FAIL_ERR
        path = os.path.basename(__file__)
        print('{0}: {1}'.format(path, err))
        exit(MOD_FAIL_ERR)

__all__ = ['main']

def main():
    # change the current directory to the one of the game
    # this is to allow executions like ``python src/tct.py''
    try:
        os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))
    except IOError as e:
        print(e)
        exit(constants.FILE_ERR)

    # get the command line options; return the option flags
    game_opts = get_parsed_opts()

    # MVC stuff
    event_manager = EventManager()
    gui_view = MainGUIView(event_manager, game_opts)

    # the game manager
    game_manager = GameManager(game_opts)

    # controller which handles the main game loop
    main_controller = MainController(event_manager, gui_view, game_manager)

    # keep running the game until a quit event occurs
    main_controller.run()

    # if control somehow reaches this point close all the pygame subsystems
    pygame.quit()
    safe_exit()


class MainController:
    '''This class is responsible for running the main game loop until a quit event occurs.'''

    def __init__(self, manager, view, gm):
        self.event_manager = manager
        self.event_manager.register_listener(self)
        self.gui_view = view
        self.game_manager = gm
        self.main_loop_running = True

    def run(self):
        while self.main_loop_running:
            # execute the game manager
            self.game_manager.run_scene()

            evt = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    evt = QuitEvent()

            # inform the event manager about the generated event
            if evt:
                self.event_manager.post(evt)

    def notify(self, event):
        if isinstance(event, QuitEvent):
            self.main_loop_running = False


class MainGUIView(Base):
    '''This class is responsible for initialising all the GUI subsystems and handling the related events.'''

    def __init__(self, manager, game_opts):
        self.event_manager = manager
        self.event_manager.register_listener(self)
        self.game_opts = game_opts
        GAME_WINDOW_TITLE = constants.GAME_PACKAGE

        # make the window of the game always centered
        os.environ["SDL_VIDEO_CENTERED"] = "1"

        pygame.init()

        pygame.display.set_mode(
            (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT),
            pygame.FULLSCREEN if self.game_opts.fullscreen else 0)
        pygame.display.set_caption(GAME_WINDOW_TITLE)
        pygame.display.set_icon(load_image(
                constants.FILES['graphics']['window']['icon'][0])[0])

        pygame.mouse.set_visible(False)

    def notify(self, event):
        '''Handle the related events.'''

if __name__ == '__main__':
    main()

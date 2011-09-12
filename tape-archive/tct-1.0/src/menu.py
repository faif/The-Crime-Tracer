# -*- coding: utf-8 -*-

#    Game's Menu Screen.
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


'''Menu Screen.

This module handles both the main and settings menus of
the game. Menus get user events and trigger operations.
'''

try:
    import random, constants, os, pygame, sound_mixer, graphics
    from os_utils import file_path, safe_exit
    from utils import get_time_sec
    from sprite_engine import *
    from credits import Credits
    from kezmenu import KezMenu
    from fsm import State
except (RuntimeError, ImportError) as err:
        import os
        from constants import MOD_FAIL_ERR
        path = os.path.basename(__file__)
        print('{0}: {1}'.format(path, err))
        exit(MOD_FAIL_ERR)

__all__ = ['Menu']


MENU_MAIN_POS_X = 525
MENU_MAIN_POS_Y = 285
MENU_KEY_DEL = 500
MENU_KEY_INT = 200
MENU_CLOCK_TICK = 50

SPRITE_SPEED = 200.0
SPRITE_ALPHA = 80

MAIN_FONT_SIZE = 32
MENU_FONT_SIZE = 25

MAIN_FOCUS_COLOR = pygame.Color('brown')
SETTINGS_FOCUS_COLOR = pygame.Color('orange')

SOUND_VOL = 0.2
MAX_ALPHA = 255

class MenuSprite(HipparchusSprite):
    def __init__(self, file, position, layer, alpha, speed, area, angle):
        super(MenuSprite, self).__init__(file, position, layer, alpha, speed, area, angle)

    def update(self, interval):
        super(MenuSprite, self).update(interval)

        self.arrangeRectangle()

        if not self._limiter is None:
            self._limiter.run(self)

class Menu(State):

    def __init__(self, game_opts):
        State.__init__(self, constants.SCENES['menu'])

        self.game_opts = game_opts
        self.screen = pygame.display.get_surface() 

        self.menu_settings_running = None
        self.menu_main_running = True

        pygame.key.set_repeat(MENU_KEY_DEL, MENU_KEY_INT)

        self.menu_main_bg = graphics.load_image(
            constants.FILES['graphics']['menu']['main']['bg'][0])[0]
        self.menu_settings_bg = graphics.load_image(
            constants.FILES['graphics']['menu']['share']['bg'][0])[0]
        self.menu_box_bg = graphics.load_image(
            constants.FILES['graphics']['menu']['settings']['box'][0])[0]

        self.window_frame = graphics.load_image(
            constants.FILES['graphics']['menu']['share']['frame'][0])[0]

        self.mouse_cursor = graphics.load_image(
            constants.FILES['graphics']['menu']['share']['cursor'][0])[0]

        self.select_option_snd = sound_mixer.load_sound(
            constants.FILES['sounds']['menu']['share']['sel'][0])

        # create the main menu - string, callback function
        self.menu_main = KezMenu(self.game_opts,
                         ['Play'     , self._play_option],
                         ['Settings' , self._settings_option],
                         ['Credits'  , self._credits_option],
                         ['Quit'     , self._quit_option])

        self.menu_main.set_position(MENU_MAIN_POS_X, MENU_MAIN_POS_Y)
        self.menu_main.set_font(graphics.load_font(
            constants.FILES['fonts']['menu']['share'][0], MAIN_FONT_SIZE))
        self.menu_main.set_highlight_color(MAIN_FOCUS_COLOR)

        # create the settings menu - string, callback function
        self.menu_settings = KezMenu(self.game_opts,
                             ['Fullscreen' , self._toggle_fullscreen_option],
                             ['Sounds'     , self._toggle_sounds_option],
                             ['Music'      , self._toggle_music_option],
                             ['Back'       , self._back_option])

        # disable the menu graphic for focused options
        self.menu_settings.toggle_image()

        self.menu_settings.set_font(graphics.load_font(
            constants.FILES['fonts']['menu']['share'][0], MENU_FONT_SIZE))
        self.menu_settings.center_at(constants.SCREEN_WIDTH / 2.0,
                                     constants.SCREEN_HEIGHT / 2.0)
        self.menu_settings.set_highlight_color(SETTINGS_FOCUS_COLOR)

        self.sprites = pygame.sprite.LayeredUpdates()

        sprites_number = len(constants.FILES['graphics']['menu']['share']['anim'])
        sprite_area = self.screen.get_rect()
        sprite_limiter = LimiterFactory().getInstance('Default')
        for i in range(sprites_number):
            sprite = MenuSprite(constants.FILES['graphics']['menu']['share']['anim'][i],
                                (sprite_area.center), i, MAX_ALPHA, SPRITE_SPEED,
                                sprite_area, 'Random')
            sprite.limiter = sprite_limiter
            self.sprites.add(sprite)

        self.clock = pygame.time.Clock()


    def do_actions(self):
        while self.menu_main_running:
            bg = self.screen.blit(self.menu_main_bg, (0, 0))
            time_passed_seconds = get_time_sec(self.clock.tick(MENU_CLOCK_TICK))

            self.sprites.update(time_passed_seconds)
            self.sprites.draw(self.screen)

            self.menu_main.draw(self.screen)

            graphics.handle_mouse_cursor(self.mouse_cursor, self.screen)

            fr = self.screen.blit(self.window_frame, (0, 0))
            need_update = (bg, fr)
            pygame.display.update(need_update)
            
            events = pygame.event.get()
            self.menu_main.update(events)

            for e in events:
                if e.type == pygame.QUIT:
                    self._quit_option()
                elif e.type == pygame.KEYDOWN:
                    if self.game_opts.sound:
                        if e.key in (pygame.K_p, pygame.K_s, pygame.K_c):
                            sound_mixer.play_sound(
                                self.select_option_snd, SOUND_VOL)
                    if e.key in (pygame.K_ESCAPE, pygame.K_q):
                        self._quit_option()
                    elif e.key == pygame.K_p:
                        self._play_option()
                    elif e.key == pygame.K_s:
                        self._settings_option()
                    elif e.key == pygame.K_c:
                        self._credits_option()

    # TODO eliminate this duplicate code
    def _settings_option(self):
        '''Entry point for main menu's settings option.'''
        # each time we enter in settings
        # sub menu, set the flag to true
        self.menu_settings_running = True

        for s in self.sprites:
            s.alpha = SPRITE_ALPHA

        while self.menu_settings_running:
            bg = self.screen.blit(self.menu_settings_bg, (0, 0))

            self.menu_main.draw(self.screen)

            time_passed_seconds = get_time_sec(self.clock.tick(MENU_CLOCK_TICK))

            self.sprites.update(time_passed_seconds)
            self.sprites.draw(self.screen)
            
            menu_bg = self.screen.blit(self.menu_box_bg, (
                    (constants.SCREEN_WIDTH - self.menu_box_bg.get_width()) / 2.0,
                    (constants.SCREEN_HEIGHT - self.menu_box_bg.get_height()) / 2.0))
            self.menu_settings.draw(self.screen)

            graphics.handle_mouse_cursor(self.mouse_cursor, self.screen)
            fr = self.screen.blit(self.window_frame, (0, 0))
            need_update = (bg, menu_bg, fr)

            pygame.display.update(need_update)
            events = pygame.event.get()
            self.menu_settings.update(events)

            for e in events:
                if e.type == pygame.QUIT:
                    self._back_option()
                    self._quit_option()
                elif e.type == pygame.KEYDOWN:
                    if self.game_opts.sound:
                        if e.key in (pygame.K_f, pygame.K_s, pygame.K_m,
                                     pygame.K_b, pygame.K_ESCAPE):
                            sound_mixer.play_sound(
                                self.select_option_snd, SOUND_VOL)
                    if e.key in (pygame.K_ESCAPE, pygame.K_b):
                        self._back_option()
                    elif e.key == pygame.K_f:
                        self._toggle_fullscreen_option()
                    elif e.key == pygame.K_s:
                        self._toggle_sounds_option()
                    elif e.key == pygame.K_m:
                        self._toggle_music_option()

        for s in self.sprites:
            s.alpha = MAX_ALPHA

    def _play_option(self):
        if self.game_opts.verbose:
            print('Start a new game.')
        self.menu_main_running = False


    def check_conditions(self):
        if not self.menu_main_running:
            return constants.SCENES['level_one']
        return None


    ## entry point for main menu's credits option
    #
    # @param self the object pointer
    def _credits_option(self):

        fullname = file_path(
            constants.FILES['texts']['menu']['credits']['text'][0],
            constants.TEXTS_DIR)

        if os.access(fullname, os.F_OK) and os.access(fullname, os.R_OK):
            if self.game_opts.verbose:
                print('Go to the credits screen.')

            c = Credits(self.screen,
                        self.game_opts,
                        self.window_frame,
                        self.menu_settings_bg,
                        self.select_option_snd,
                        fullname)

            if not c.run():
                # quit if the close button is
                # pressed (inside the credits)
                self._quit_option()
        else:
            path = os.path.basename(__file__)
            print("{0}: couldn't read text file: {1}".format(path, fullname))
            raise SystemExit

    def _quit_option(self):
        if self.game_opts.verbose:
            print('Exit the game!')

        # perform safe exit
        safe_exit()

    def _toggle_fullscreen_option(self):
        self.game_opts.fullscreen = not self.game_opts.fullscreen

        if self.game_opts.verbose:
            print('Toggle fullscreen!')

        mouse_position = pygame.mouse.get_pos()

        pygame.display.set_mode(
            (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT),
            pygame.FULLSCREEN if self.game_opts.fullscreen else 0)

        pygame.mouse.set_pos(mouse_position)

    def _toggle_sounds_option(self):
        self.game_opts.sound = not self.game_opts.sound
        if self.game_opts.verbose:
            print('Toggle sounds!')

    def _toggle_music_option(self):
        if self.game_opts.verbose:
            print('Toggle music!')

        self.game_opts.music = not self.game_opts.music
        if self.game_opts.music:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

    def _back_option(self):
        self.menu_settings_running = False
        if self.game_opts.verbose:
            print('Go back to main menu!')

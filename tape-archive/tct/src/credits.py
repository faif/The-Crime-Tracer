# -*- coding: utf-8 -*-

#    Credits Screen.
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


''' A Credits Screen.

This module contains the menu's credits screen implementation.
'''

try:
    import constants, pygame
    from pygame.locals import *
    from base import Base
    from sound_mixer import load_sound, play_sound
    from graphics import load_font
    from utils import get_time_sec
except (RuntimeError, ImportError) as err:
        import os
        from constants import MOD_FAIL_ERR
        path = os.path.basename(__file__)
        print('{0}: {1}'.format(path, err))
        exit(MOD_FAIL_ERR)

__all__ = ['Credits']

# mapping markup font size token tags with size and color
SIZE_TAGS = {"[XL]":     [60, pygame.Color('white')],
             "[LARGE]":  [50, pygame.Color('cadetblue')],
             "[MEDIUM]": [40, pygame.Color('black')],
             "[SMALL]":  [30, pygame.Color('brown')]}

# the next variable value must be synchronized
# with the first key of the previous structure

# the space between line texts
LINESPACE = SIZE_TAGS["[XL]"][0]

# mapping markup main authors token tags with real names
AUTH_TAGS = {"[LAFS]": "Efstathios Xatzikiriakidis",
             "[FAIF]": "Sakis Kasampalis"}

# the credits text file comment character 
CREDITS_COMMENT_TOKEN = "#"

# the default size of a text item
FONT_SIZE = 20

# the default color of a text item
FONT_COLOR = pygame.Color('black')

SOUND_VOL = 0.2
SCROLL_SPEED = 50
SCROLL_FACTOR = 100

class TextItem(Base):

    def __init__(self, parent, surface, text, vertical,
                 size=FONT_SIZE, color=FONT_COLOR):
        self.parent = parent
        self.surface = surface
        self.text = text
        self.color = color
        self.vertical = vertical
        self.font = load_font(
            constants.FILES['fonts']['menu']['share'][3], size)
        # render the text with the appropriate attributes
        self.text = self.font.render(self.text, True, self.color)
        # set the x coordinate (horizontally in the middle)
        self.x = (self.surface.get_width() - self.text.get_width()) / 2.0

    def redraw(self):
        # set the y coordinate (vertically to the bottom + vertical offset)
        y = self.parent.scroll_root + self.vertical

        # blit the text at x, y on the surface given
        self.surface.blit(self.text, (self.x, y))

class Credits(Base):

    def __init__(self, screen, game_opts, frame, bg, sound, textfile):
        self.screen = screen
        self.game_opts = game_opts
        self.window_frame = frame
        self.credits_bg = bg
        self.return_sound = sound
        self.credits_running = None
        self.text_items = []
        self.bg_x_pos = 0
        self.height = 0
        # the scroll root starts from the bottom of the screen
        self.scroll_root = self.screen.get_height()
        self.scroll_speed = SCROLL_SPEED
        # the speed of the background movement; it's nice
        # for the eye to be the same as the scroll speed
        self.background_speed = self.scroll_speed

        with open(textfile) as fin:
            # parse each line, interpreter markup tokens, create text items
            for line in fin:

                # strip all white characters from right and left
                line = line.strip()

                # ignore lines having as first non
                # white character the comment one
                if line.startswith(CREDITS_COMMENT_TOKEN):
                    # go to the next line
                    continue

                # interpret main authors token tags
                for token_tag in AUTH_TAGS:
                    # check if the author token tag exists in the line
                    if token_tag in line:
                        # replace the username with the real name
                        line = line.replace(token_tag, AUTH_TAGS[token_tag])
                        # we accept only one author token tag on each line
                        break

                # interpret font sizes token tags and create text items
                for token_tag in SIZE_TAGS:
                    # check if the font size token tag exists in the line
                    if token_tag in line:
                        # remove the font size token tag
                        line = line.replace(token_tag, "")

                        # create the appropriate rendered text item
                        newtext = TextItem(self,
                                           self.screen,
                                           line,
                                           self.height,
                                           SIZE_TAGS[token_tag][0],
                                           SIZE_TAGS[token_tag][1])

                        # we accept only one font size token tag per line
                        break
                    # if the line has no markup token tag render text as default
                    else:
                        # create the default rendered text item
                        newtext = TextItem(self, self.screen, line, self.height)

                # add text item to the list
                self.text_items.append(newtext)

                # the linespace between lines
                # should be the max font size
                self.height += LINESPACE

        self.clock = pygame.time.Clock()

    def run(self):
        self.credits_running = True

        # display & update screen, get all the events
        while self.credits_running:
            # redraw the credits screen
            need_update = self._redraw()

            # count time passed in seconds
            time_passed_seconds = get_time_sec(self.clock.tick())

            # update the screen objects' position
            self._update(time_passed_seconds)

            # display the screen surface
            pygame.display.update(need_update)

            # get all the events and operate properly
            for e in pygame.event.get():
                # quit when the close button is pressed
                if e.type == pygame.QUIT:
                    # force caller to terminate the game
                    return False

            # handle keyboard keys
            key = pygame.key.get_pressed()
            if key[K_ESCAPE] or key[K_q]:
                self.credits_running = False
                if self.game_opts.sound:
                    play_sound(self.return_sound, SOUND_VOL)

        # credits screen returns normally
        return True

    def _update(self, seconds):
        '''Update the screen objects' position.

        Arguments:
        seconds -- the time factor to use for moving the objects
        '''
        # normal scrolling
        if self.scroll_root > self.screen.get_height() - self.height - SCROLL_FACTOR:
            self.scroll_root -= (self.scroll_speed * seconds)

        # slow down as the end approaches
        elif self.scroll_root > self.screen.get_height() / 2.0 - self.height:
            self.scroll_root -= (self.scroll_speed * seconds / 2.0)

        # move the background image
        self.bg_x_pos -= (self.background_speed * seconds)

        # correct the x coordinate of the background image
        if self.bg_x_pos < -self.credits_bg.get_width():
            self.bg_x_pos = 0

    def _redraw(self):
        bg = self.screen.blit(self.credits_bg, (self.bg_x_pos, 0))

        # blit the continuation of the background image
        if self.bg_x_pos < - (self.credits_bg.get_width() -
                              self.screen.get_width()):
            bg_cont = self.screen.blit(self.credits_bg, (self.bg_x_pos +
                             self.credits_bg.get_width(), 0))

        tuple(item.redraw() for item in self.text_items)

        # draw the frame of the window
        fr = self.screen.blit(self.window_frame, (0, 0))

        # pass bg_cont only if defined
        if 'bg_cont' in locals():
            need_update = (bg, bg_cont, fr)
        else:
            need_update = (bg, fr)

        return need_update

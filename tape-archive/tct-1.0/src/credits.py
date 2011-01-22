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


## @package credits
#  Game's Credits Screen.
#
# This module contains the game's credits screen implementation.


try:
    import constants, pygame
    from pygame.locals import *
    from base import Base
    from sound_mixer import load_sound, play_sound
    from graphics import load_image, load_font
    from utils import get_time_sec
    from os_utils import fopen
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
__all__ = ['Credits']


## mapping markup font size token tags with size and color
SIZE_TAGS = {"[XL]":     [60, pygame.Color('white')],
             "[LARGE]":  [50, pygame.Color('cadetblue')],
             "[MEDIUM]": [40, pygame.Color('black')],
             "[SMALL]":  [30, pygame.Color('brown')]}

# the next variable value must be synchronized
# with the first key of the previous structure

## the space between line texts
LINESPACE = SIZE_TAGS["[XL]"][0]

## mapping markup main authors token tags with real names
AUTH_TAGS = {"[LAFS]": "Efstathios Xatzikiriakidis",
             "[FAIF]": "Sakis Kasampalis"}

## the credits text file comment character 
CREDITS_COMMENT_TOKEN = "#"

## the default size of a text item
FONT_SIZE = 20

## the default color of a text item
FONT_COLOR = pygame.Color('black')

SOUND_VOL = 0.2
SCROLL_SPEED = 50
SCROLL_FACTOR = 100


## class for creating text items
#
class TextItem(Base):

    ## initialize the text item
    #
    # @param self the object pointer
    # @param parent the parent's object pointer
    # @param surface the surface used for blitting
    # @param text the text itself
    # @param vertical the vertical offset of the text
    # @param size the size of the text item
    # @param color the color of the text item
    def __init__(self, parent, surface, text, vertical,
                 size=FONT_SIZE, color=FONT_COLOR):
        ## store the parent object
        self.parent = parent

        ## store the surface
        self.surface = surface

        ## store the text
        self.text = text

        ## store the color
        self.color = color

        ## store the vertical offset
        self.vertical = vertical

        ## set the font and size used for the text
        self.font = load_font(
            constants.FILES['fonts']['menu']['share'][3], size)

        # render the text with the appropriate attributes
        self.text = self.font.render(self.text, True, self.color)

        ## set the x coordinate (horizontally in the middle)
        self.x = (self.surface.get_width() - self.text.get_width()) / 2.0

    ## draw the text item
    #
    # @param self the object pointer
    def redraw(self):
        # set the y coordinate (vertically to the bottom + vertical offset)
        y = self.parent.scroll_root + self.vertical

        # blit the text at x, y on the surface given
        self.surface.blit(self.text, (self.x, y))


## class for game's credits screen
#
class Credits(Base):

    ## initialize the credits screen
    #
    # @param self the object pointer
    # @param screen the screen surface
    # @param game_opts the game's command line options
    # @param frame the window frame preloaded image
    # @param bg the credits background preloaded image
    # @param sound the preloaded sound on exit
    # @param textfile the file with the text content
    def __init__(self, screen, game_opts, frame, bg, sound, textfile):
        ## get the screen surface
        self.screen = screen

        ## the game's command line options
        self.game_opts = game_opts

        ## set the window frame
        self.window_frame = frame

        ## set the credits screen background
        self.credits_bg = bg

        ## set the sound when we return back to the caller
        self.return_sound = sound

        ## flag to control the credits loop
        self.credits_running = None

        ## the list with the rendered text items
        self.text_items = []

        ## set the initial background image x coordinate
        self.bg_x_pos = 0

        ## the total height of the rendered text content
        self.height = 0

        ## the scroll root starts from the bottom of the screen
        self.scroll_root = self.screen.get_height()

        ## the speed of the scroll movement
        self.scroll_speed = SCROLL_SPEED

        ## the speed of the background movement it's nice
        ## for the eye to be the same as the scroll speed
        self.background_speed = self.scroll_speed

        # ensure that the file can be opened without problems
        fin = fopen(textfile)

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

        ## create clock and track time
        self.clock = pygame.time.Clock()


    ## run the loop of the credits screen
    #
    # @param self the object pointer
    # @return inform caller to quit or not
    def run(self):
        # flag to control the credits loop
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
            # when user presses escape key or 'q'uit key
            if key[K_ESCAPE] or key[K_q]:
                self.credits_running = False

                # play the return sound
                if self.game_opts.sound:
                    play_sound(self.return_sound, SOUND_VOL)

        # credits screen returns normally
        return True

    ## update the screen objects' position
    #
    # @param self the object pointer
    # @param seconds the time factor to use for moving the objects
    def _update(self, seconds):
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

    ## redraw the credits screen
    #
    # @param self the object pointer
    def _redraw(self):

        # draw the background image
        bg = self.screen.blit(self.credits_bg, (self.bg_x_pos, 0))

        # blit the continuation of the background image
        if self.bg_x_pos < - (self.credits_bg.get_width() -
                              self.screen.get_width()):

            bg_cont = self.screen.blit(self.credits_bg, (self.bg_x_pos +
                             self.credits_bg.get_width(), 0))

        # draw each text item
        [item.redraw() for item in self.text_items]

        # draw the frame of the window
        fr = self.screen.blit(self.window_frame, (0, 0))

        # pass bg_cont only if defined
        if 'bg_cont' in locals():
            need_update = (bg, bg_cont, fr)
        else:
            need_update = (bg, fr)

        return need_update


# test the script if executed
if __name__ == '__main__':
    import sys
    print((' '.join(('Testing', sys.argv[0]))))
    TextItem('parent', 'surface', 'text', 0)

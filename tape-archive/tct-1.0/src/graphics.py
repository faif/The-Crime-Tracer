# -*- coding: utf-8 -*-

#    Game's Graphics Utilities.
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


## @package graphics
#  Graphics Utilities.
#
# This module contains the game's graphics
# utilities, loading graphics, fonts, etc.


try:
    import constants, pygame
    from pygame.locals import RLEACCEL
    from os_utils import file_path
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
__all__ = ['load_image', 'load_font', 'handle_mouse_cursor']


## the default size of a font
FONT_SIZE = 17

## the default colorkey of an image
IMAGE_COLORKEY = None


## load an image with an optional colorkey
#
# @param filename the filename of the image
# @param colorkey the RGB value of the colorkey, or -1
#                 to get the topleft of the given image 
# @throw SystemExit if the load fails
# @return the loaded image and its coordinates
def load_image(filename, colorkey=IMAGE_COLORKEY):
    # get the path of the filename
    fullname = file_path(filename, constants.GRAPHICS_DIR)

    # try to load the image
    try:
        image = pygame.image.load(fullname)
    except:
        import os
        path = os.path.basename(__file__)
        print((': '.join((path, "couldn't load image", fullname))))
        raise SystemExit

    # check the current alpha value of the surface
    if image.get_alpha() is None:
        image = image.convert()
    else:
        image = image.convert_alpha()

    # check for image's colorkey
    if colorkey:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)

    return image, image.get_rect()


## load a font
#
# @param filename the filename of the font
# @param size the size of the font
# @throw SystemExit if the load fails
# @return the loaded font
def load_font(filename, size=FONT_SIZE):
    # get the path of the filename
    fullname = file_path(filename, constants.FONTS_DIR)

    # try to create the font
    try:
        font = pygame.font.Font(fullname, size)
    except:
        import os
        path = os.path.basename(__file__)
        print((': '.join((path, "couldn't load font", fullname))))
        raise SystemExit

    return font


## update the custom cursor
#
# @param mc the mouse cursor
# @param su the surface used for blitting
def handle_mouse_cursor(mc, su):
    x, y = pygame.mouse.get_pos()
    x -= mc.get_width() / 2.0
    y -= mc.get_height() / 2.0
    su.blit(mc, (x, y))

# -*- coding: utf-8 -*-

#    Graphics Utilities.
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

'''Graphics Utilities.

This module contains graphics utilities for loading graphics, fonts, etc.
'''

try:
    import pygame, constants
    from pygame.locals import RLEACCEL
    from os_utils import file_path
except (RuntimeError, ImportError) as err:
        import os
        from constants import MOD_FAIL_ERR
        path = os.path.basename(__file__)
        print('{0}: {1}'.format(path, err))
        exit(MOD_FAIL_ERR)

__all__ = ['load_image', 'load_font', 'handle_mouse_cursor']

FONT_SIZE = 17
IMAGE_COLORKEY = None

def load_image(filename, colorkey=IMAGE_COLORKEY):
    fullname = file_path(filename, constants.GRAPHICS_DIR)

    try:
        image = pygame.image.load(fullname)
    except pygame.error as err:
        import os
        path = os.path.basename(__file__)
        print("{0}: couldn't load image: {1} ".format(path, fullname))
        raise SystemExit

    if image.get_alpha() is None:
        image = image.convert()
    else:
        image = image.convert_alpha()

    if colorkey:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)

    return image, image.get_rect()


def load_font(filename, size=FONT_SIZE):
    fullname = file_path(filename, constants.FONTS_DIR)

    try:
        font = pygame.font.Font(fullname, size)
    except IOError as err:
        import os
        path = os.path.basename(__file__)
        print("{0}: couldn't load font: {1}".format(path, fullname))
        raise SystemExit

    return font

def handle_mouse_cursor(mc, su):
    '''update the custom mouse cursor'''
    x, y = pygame.mouse.get_pos()
    x -= mc.get_width() / 2.0
    y -= mc.get_height() / 2.0
    su.blit(mc, (x, y))

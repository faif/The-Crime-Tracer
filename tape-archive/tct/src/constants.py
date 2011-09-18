#  -*- coding: utf-8 -*-

#    Global Reusable Constants.
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


'''Global Reusable Constants.

This module contains some reusable constants
which are imported in many places of the game.
'''
from os import path

'''error return codes'''
# the module failure exit error signal
MOD_FAIL_ERR = 1

# the module import error exit signal
MOD_IMP_ERR = 2

# the file cannot be found, accessed, etc. (IOError)
FILE_ERR = 3

GAME_VERSION = '1.0'
GAME_TITLE = 'the crime tracer, the suspect passer-by'.title()
GAME_PACKAGE = '{0} (VER-{1})'.format(GAME_TITLE,  GAME_VERSION)

'''basic directories'''
RESOURCES_DIR = 'resources'
GRAPHICS_DIR = 'graphics'
FONTS_DIR = 'fonts'
SOUNDS_DIR = 'sounds'
TEXTS_DIR = 'texts'

'''sub directories'''
INTRO_DIR = 'intro'
MENU_DIR = 'menu'
SHARE_DIR = 'share'

'''game resolution'''
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

'''scene names'''
SCENES = { 'intro':'introduction', 'menu':'main menu', 'level_one': 'first level' }

'''game resource filenames'''
FILES = { 'graphics': {
            'intro': {
                'slides': (path.join(INTRO_DIR, 'ct-intro-slide-0.jpg'),
                           path.join(INTRO_DIR, 'ct-intro-slide-1.jpg'),
                           path.join(INTRO_DIR, 'ct-intro-slide-2.jpg')),
                'blank': [path.join(INTRO_DIR, 'ct-intro-blank-0.jpg')]
            },
            'menu': {
              'main': {
                  'bg': [path.join(MENU_DIR, 'ct-menu-main-bg-0.jpg')]
              },
              'settings': {
                  'box': [path.join(MENU_DIR, 'ct-menu-sets-box-bg-0.png')]
              },
              'share': {
                  'frame': [path.join(MENU_DIR, 'ct-window-frame-0.png')],
                  'bg': [path.join(MENU_DIR, 'ct-menu-sets-bg-0.jpg')],
                  'cursor': [path.join(SHARE_DIR, 'ct-menu-mouse-0.png')],
                  'anim': (path.join(MENU_DIR, 'ct-window-animation-0.png'),
                           path.join(MENU_DIR, 'ct-window-animation-1.png')),
                  'focus': [path.join(MENU_DIR, 'ct-menu-hover-0.png')]
              }
            },
            'window': {
                'icon': [path.join(SHARE_DIR, 'ct-window-icon-0.png')]
            }
          },
          'sounds': {
            'menu': {
              'share': {
                  'bg': [path.join(MENU_DIR, 'ct-menu-bg-sound-0.ogg')],
                  'sel': [path.join(MENU_DIR, 'ct-menu-sound-select-0.ogg')],
                  'focus': [path.join(MENU_DIR, 'ct-menu-sound-focus-0.ogg')]
              }
            }
          },
          'fonts': {
            'menu': {
                'share': ('ct-menu-font-0.ttf',
                          'ct-menu-font-1.ttf',
                          'ct-menu-font-2.ttf',
                          'ct-menu-font-3.ttf')
            }
          },
          'texts': {
            'menu': {
              'credits': {
                  'text': ['ct-credits-data.txt']
              }
            }
          }
        }

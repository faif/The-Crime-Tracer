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


## @package constants
#  Game's Global Reusable Constants.
#
# This module contains some reusable constants
# which are imported in many places of the game.


# game error return codes

## the module failure exit error signal
MOD_FAIL_ERR = 1

## the module import error exit signal
MOD_IMP_ERR = 2

## the file cannot be found, accessed, etc. (IOError)
FILE_ERR = 3

try:
    from os import path
# importing os failed, print a custom message...
except ImportError as err:
    print((': '.join(("couldn't load module", str(err)))))
    exit(MOD_IMP_ERR)

# game package info

## the game's version
GAME_VERSION = '1.0'

## the game's title
GAME_TITLE = 'the crime tracer, the suspect passer-by'.title()

## the game's package
GAME_PACKAGE = ' '.join((GAME_TITLE, '(V %s).' % (GAME_VERSION)))

# basic directories

## resources directory
RESOURCES_DIR = 'resources'

## graphics directory
GRAPHICS_DIR = 'graphics'

## fonts directory
FONTS_DIR = 'fonts'

## sounds directory
SOUNDS_DIR = 'sounds'

## texts directory
TEXTS_DIR = 'texts'

# sub directories

## introduction directory
INTRO_DIR = 'intro'

## menu directory
MENU_DIR = 'menu'

## share directory
SHARE_DIR = 'share'

# game resolution

## game's screen width
SCREEN_WIDTH = 800

## game's screen height
SCREEN_HEIGHT = 600

## the scene names
SCENES = { 'intro':'introduction', 'menu':'main menu', 'level_one': 'first level' }

# game resources' filenames

## the structure of game's resources filenames
FILES = { 'graphics': {
            'intro': {
                # the intro slides' filenames
                'slides': (path.join(INTRO_DIR, 'ct-intro-slide-0.jpg'),
                           path.join(INTRO_DIR, 'ct-intro-slide-1.jpg'),
                           path.join(INTRO_DIR, 'ct-intro-slide-2.jpg')),

                # the intro blank slide filename
                'blank': [path.join(INTRO_DIR, 'ct-intro-blank-0.jpg')]
            },
            'menu': {
              'main': {
                  # the main menu's background filenames
                  'bg': [path.join(MENU_DIR, 'ct-menu-main-bg-0.jpg')]
              },
              'settings': {
                  # the settings menu's background box filenames
                  'box': [path.join(MENU_DIR, 'ct-menu-sets-box-bg-0.png')]
              },
              'share': {
                  # the window's frame filenames
                  'frame': [path.join(MENU_DIR, 'ct-window-frame-0.png')],

                  # the settings menu's background filenames
                  'bg': [path.join(MENU_DIR, 'ct-menu-sets-bg-0.jpg')],

                  # the mouse cursor filenames
                  'cursor': [path.join(SHARE_DIR, 'ct-menu-mouse-0.png')],

                  # the animation sprites filenames
                  'anim': (path.join(MENU_DIR, 'ct-window-animation-0.png'),
                           path.join(MENU_DIR, 'ct-window-animation-1.png')),

                  # the menu's focus filenames
                  'focus': [path.join(MENU_DIR, 'ct-menu-hover-0.png')]
              }
            },
            'window': {
                # the icon (in window mode) filenames
                'icon': [path.join(SHARE_DIR, 'ct-window-icon-0.png')]
            }
          },
          'sounds': {
            'menu': {
              'share': {
                  # the menu's background music filenames
                  'bg': [path.join(MENU_DIR, 'ct-menu-bg-sound-0.ogg')],

                  # the menu's select filenames
                  'sel': [path.join(MENU_DIR, 'ct-menu-sound-select-0.ogg')],

                  # the menu's focus filenames
                  'focus': [path.join(MENU_DIR, 'ct-menu-sound-focus-0.ogg')]
              }
            }
          },
          'fonts': {
            'menu': {
                # the menu's custom font filenames
                'share': ('ct-menu-font-0.ttf',
                          'ct-menu-font-1.ttf',
                          'ct-menu-font-2.ttf',
                          'ct-menu-font-3.ttf')
            }
          },
          'texts': {
            'menu': {
              'credits': {
                  # the main menu's credits text file
                  'text': ['ct-credits-data.txt']
              }
            }
          }
        }

# game information

## the GNU GPL license of the game
GAME_GPL = (
  "Copyright (C) 2009-11 Free Software Gaming Geeks <fsgamedev@googlegroups.com>",
  " ",
  "This program is free software: you can redistribute it and/or modify",
  "it under the terms of the GNU General Public License as published by",
  "the Free Software Foundation, either version 3 of the License, or",
  "(at your option) any later version.",
  " ",
  "This program is distributed in the hope that it will be useful,",
  "but WITHOUT ANY WARRANTY; without even the implied warranty of",
  "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the",
  "GNU General Public License for more details.",
  " ",
  "You should have received a copy of the GNU General Public License",
  "along with this program.  If not, see <http://www.gnu.org/licenses/>."
)

## the authors of the game
GAME_AUTHORS = (
  "Sakis Kasampalis <faif at dtek period gr>",
  "Efstathios Xatzikiriakidis <contact at efxa period gr>",
  "Nikolaos Delis <delis89 at gmail period com>",
  "Dimitris Ventas <rayone99 at gmail period com>",
  "Mihalis Kasampalis <michaelkas at hotmail period com>"
)

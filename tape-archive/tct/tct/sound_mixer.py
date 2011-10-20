# -*- coding: utf-8 -*-

#    Sound Mixer.
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


'''Sound Mixer.

This module contains utilities which support
background music and small streaming sounds.
'''

try:
    import constants, pygame, os
    from os_utils import file_path
except (RuntimeError, ImportError) as err:
        import os
        from constants import MOD_FAIL_ERR
        path = os.path.basename(__file__)
        print('{0}: {1}'.format(path, err))
        exit(MOD_FAIL_ERR)

__all__ = ['play_music', 'play_sound']

SOUND_VOLUME = 0.1
MUSIC_REPEAT = -1

# initialize the sound mixer
pygame.mixer.pre_init(44100, -16, 2, 4096)

def load_sound(filename):
    fullname = file_path(filename, constants.SOUNDS_DIR)

    if not os.path.isfile(fullname):
        raise SystemExit('Not a file: {0}'.format(fullname))

    sound = pygame.mixer.Sound(fullname)

    return sound

def play_music(filename, repeat=MUSIC_REPEAT):
    '''Play a background audio theme'''
    fullname = file_path(filename, constants.SOUNDS_DIR)

    try:
        sound = pygame.mixer.music.load(fullname)
        pygame.mixer.music.play(repeat)
    except pygame.error as err:
        import os
        path = os.path.basename(__file__)
        raise SystemExit("{0}: couldn't load music: {1}".format(path, fullname))

def play_sound(sound, volume=SOUND_VOLUME):
    '''Play a non streaming sound.'''
    # handle the exception when the keys
    # are pressed too fast by the user
    try:
        channel = sound.play()
        channel.set_volume(volume)
    except AttributeError as err:
        print('{0}'.format(err))

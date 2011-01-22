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


## @package sound_mixer
#  Sound Mixer.
#
# This module contains utilities which support
# background music and small streaming sounds.


try:
    import constants, pygame
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
__all__ = ['play_music', 'play_sound']


## the default volume of a non stream sound
SOUND_VOLUME = 0.1

## the default number of times to play a music
MUSIC_REPEAT = -1


# initialize the sound mixer
pygame.mixer.pre_init(44100, -16, 2, 4096)


## load a sound
#
# @param filename the filename of the sound
# @throw SystemExit when the sound's load fails
# @return the loaded sound
def load_sound(filename):
    # get the path of the filename
    fullname = file_path(filename, constants.SOUNDS_DIR)

    # try to load the sound
    try:
        sound = pygame.mixer.Sound(fullname)
    except:
        print((' '.join(("Couldn't load sound:", fullname))))
        raise SystemExit

    # return the loaded sound
    return sound


## play a background music
#
# @param filename the filename of the music
# @param repeat how many times to play the
#               music, default is forever
# @throw SystemExit when the load fails
def play_music(filename, repeat=MUSIC_REPEAT):
    # get the path of the filename
    fullname = file_path(filename, constants.SOUNDS_DIR)

    # try to play the music theme
    try:
        sound = pygame.mixer.music.load(fullname)
        pygame.mixer.music.play(repeat)
    except:
        print((' '.join(("Couldn't play music:", fullname))))
        raise SystemExit


## play a non streaming sound
#
# @param sound the sound file to play
# @param volume the volume of the sound channel
def play_sound(sound, volume=SOUND_VOLUME):
    # handle the exception when the keys
    # are pressed too fast by the user
    try:
        # play the sound given
        channel = sound.play()

        # set volume as given
        channel.set_volume(volume)
    except AttributeError:
        print('No sound channels available!')

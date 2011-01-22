# -*- coding: utf-8 -*-

#    Linear Sprite Animation Utils.
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


## @package anim_sprite
#  Game's Linear Sprite Animation Utils.
#
# This module contains some classes which
# provide linear sprite animation motion.

try:
    import constants, pygame.sprite
    from random import seed, randint
    from datetime import datetime
    from graphics import load_image
    from base import Base
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
__all__ = ['SpriteFactory']

## enum-like constants
VERTICAL_ANIMATION, HORIZONTAL_ANIMATION = \
    list(range(len(constants.FILES['graphics']['menu']['share']['anim'])))

## the "right" way to create a new sprite (exposed interface)
#
class SpriteFactory(Base):

    ## create a new animated sprite at an optional given position
    #
    # @param self the object pointer
    # @param file the sprite's image filename
    # @param speed the sprite's speed movement
    # @param pos the sprite's initial position
    # @return the requested sprite instance
    # @throw ValueError if the requested sprite type is wrong
    def create_anim_sprite(self, type, file, speed, pos=[0, 0]):
        if (type == VERTICAL_ANIMATION):
            return VertAnimSprite(file, pos, speed)
        elif (type == HORIZONTAL_ANIMATION):
            return HorAnimSprite(file, pos, speed)
        else:
            raise ValueError('Incorrect sprite type', type)


## a static sprite - the base class of all
#
class SSprite(pygame.sprite.Sprite):

    ## create a new static sprite
    #
    # @param self the object pointer
    # @param image the sprite's image filename
    # @param init_pos the sprite's initial position
    def __init__(self, image, init_pos):
        # call the base sprite constructor
        pygame.sprite.Sprite.__init__(self)

        ## the sprite's image
        self.image = load_image(image)[0]

        ## the sprite's rectangle structure
        self.rect = self.image.get_rect()

        ## the sprite's initial position
        self.rect.topleft = init_pos


## an animated sprite - the base class of animations
#
class AnimSprite(SSprite):

    ## create a new animated sprite
    #
    # @param self the object pointer
    # @param image the sprite's image filename
    # @param init_pos the sprite's initial position
    # @param speed the sprite's speed movement
    def __init__(self, image, init_pos, speed):
        # call the base static sprite constructor
        SSprite.__init__(self, image, init_pos)

        # set up a random seed based on microseconds
        seed(datetime.now().microsecond)

        ## the sprite's speed movement
        self.speed = speed

        ## restrict the sprite's motion within the screen
        self.area = pygame.display.get_surface().get_rect()

        ## the distance moved since the last movement
        self.distance_moved = 0.0

    ## calculate the new distance for moving the sprite
    #
    # @param self the object pointer
    # @param time_pass_sec updated time since last movement in seconds
    def update(self, time_pass_sec):
        self.distance_moved = time_pass_sec * self.speed


## a vertical animated sprite
#
class VertAnimSprite(AnimSprite):

    ## create a new vertical animated sprite
    #
    # @param self the object pointer
    # @param image the sprite's image filename
    # @param init_pos the sprite's initial position
    # @param speed the sprite's speed movement
    def __init__(self, image, init_pos, speed):
        # call the base animated sprite constructor
        AnimSprite.__init__(self, image, init_pos, speed) 

        ## random number constraint
        self.limit = self.image.get_width()

    ## move the sprite to a new position
    #
    # @param self the object pointer
    # @param time_pass_sec updated time since last movement in seconds
    def update(self, time_pass_sec):
        # call the base animated sprite update
        AnimSprite.update(self, time_pass_sec)
        
        # update the sprite's position
        self.rect.move_ip(0, self.distance_moved)

        # if the sprite is out of screen update its place
        # to a new random (but still within the screen)        
        if self.rect.top >= self.area.bottom:
            self.rect.left = randint(self.area.left + self.limit,
                                     self.area.right - self.limit) 
            self.rect.top = self.area.top - self.area.bottom


## a horizontal animate sprite
#
class HorAnimSprite(AnimSprite):

    ## create a new horizontal animated sprite
    #
    # @param self the object pointer
    # @param image the sprite's image filename
    # @param init_pos the sprite's initial position
    # @param speed the sprite's speed movement
    def __init__(self, image, init_pos, speed):
        # call the base animated sprite constructor
        AnimSprite.__init__(self, image, init_pos, speed) 

        ## random number constraint
        self.limit = self.image.get_height()

    ## move the sprite to a new position
    #
    # @param self the object pointer
    # @param time_pass_sec updated time since last movement in seconds
    def update(self, time_pass_sec):
        # call the base animated sprite update
        AnimSprite.update(self, time_pass_sec)

        # update the sprite's position
        self.rect.move_ip(self.distance_moved, 0)

        # if the sprite is out of screen update its place
        # to a new random (but still within the screen)        
        if self.rect.left >= self.area.right:
            self.rect.left = self.area.left - self.area.right
            self.rect.top = randint(self.area.top + self.limit,
                                    self.area.bottom - self.limit)

# test the script if executed
if __name__ == '__main__':
    import sys
    print((' '.join(('Testing', sys.argv[0]))))

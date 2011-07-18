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


'''Linear Sprite Animation Utils.

This module contains some classes which
provide linear sprite animation motion.
'''

try:
    from random import seed, randint
    from datetime import datetime
    import pygame.sprite
    from graphics import load_image
    from base import Base
    import constants 
except ImportError as err:
    try:
        import os
        path = os.path.basename(__file__)
        print((': '.join((path, str(err)))))
    except ImportError:
        print((': '.join(("couldn't load module", str(err)))))
    exit(2)

# TODO: leave only SpriteFactory (the rest are temporary for
# demonstrating docstrings)
__all__ = ['SpriteFactory', 'SSprite', 'AnimSprite', 
           'VertAnimSprite', 'HorAnimSprite']

VERT_ANIM, HORIZ_ANIM = \
    list(range(len(constants.FILES['graphics']['menu']['share']['anim'])))

MAX_SPEED = 220.0
MIN_SPEED = 100.0

class SpriteFactory(Base):
    '''The "right" way to create a new sprite (exposed interface).'''

    def create_anim_sprite(self, type, file, speed, pos=[0, 0]):
        '''Create a new animated sprite at an optional given position.

        Arguments:
        type -- the animation style (vertical, horizontal, etc)
        file -- the sprite's image filename
        speed -- the sprite's speed movement
        pos -- the sprite's initial position

        Exceptions: ValueError if 1) the requested sprite type is 
        wrong, 2) the speed value is > max. or < min. acceptable.

        Return: SSprite if everything is fine, None otherwise.
        '''
        if speed < MIN_SPEED or speed > MAX_SPEED:
            raise SpriteSpeedError('Incorrect sprite speed value', speed)

        if (type == VERT_ANIM):
            return VertAnimSprite(file, pos, speed)
        elif (type == HORIZ_ANIM):
            return HorAnimSprite(file, pos, speed)
        else:
            raise SpriteTypeError('Incorrect sprite type', type)


class SSprite(pygame.sprite.Sprite):
    '''A static sprite - the base class of all sprites.'''

    def __init__(self, image, init_pos):
        '''Create a new static sprite.

        Arguments:
        image -- the sprite's image filename
        init_pos -- the sprite's initial position
        '''
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(image)[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos


class AnimSprite(SSprite):
    '''An animated sprite - the base class of animations.'''

    def __init__(self, image, init_pos, speed):
        '''Create a new animated sprite.

        Arguments:
        image -- the sprite's image filename
        init_pos -- the sprite's initial position
        speed -- the sprite's speed movement
        '''
        SSprite.__init__(self, image, init_pos)

        # set up a random seed based on microseconds
        seed(datetime.now().microsecond)

        self.speed = speed

        # restrict the sprite's motion within the screen
        self.area = pygame.display.get_surface().get_rect()

        # the distance moved since the last movement
        self.distance_moved = 0.0


    def update(self, time_pass_sec):
        '''Calculate the new distance for moving the sprite.

        Arguments:
        time_pass_sec -- updated time since the last movement in seconds
        '''
        self.distance_moved = time_pass_sec * self.speed


class VertAnimSprite(AnimSprite):
    '''A vertical animated sprite.'''

    def __init__(self, image, init_pos, speed):
        '''Create a new vertical animated sprite.
        
        Arguments:
        image -- the sprite's image filename
        init_pos -- the sprite's initial position
        speed -- the sprite's speed movement
        '''
        AnimSprite.__init__(self, image, init_pos, speed) 

        # random number constraint
        self.limit = self.image.get_width()


    def update(self, time_pass_sec):
        '''Move the sprite to a new position.

        Arguments:
        time_pass_sec -- updated time since last movement in seconds
        '''
        AnimSprite.update(self, time_pass_sec)
        
        # update the sprite's position
        self.rect.move_ip(0, self.distance_moved)

        # if the sprite is out of screen update its place
        # to a new random (but still within the screen)        
        if self.rect.top >= self.area.bottom:
            self.rect.left = randint(self.area.left + self.limit,
                                     self.area.right - self.limit) 
            self.rect.top = self.area.top - self.area.bottom


class HorAnimSprite(AnimSprite):
    '''A horizontal animated sprite.'''

    def __init__(self, image, init_pos, speed):
        '''Create a new horizontal animated sprite.

        Arguments:
        image -- the sprite's image filename
        init_pos -- the sprite's initial position
        speed -- the sprite's speed movement
        '''
        AnimSprite.__init__(self, image, init_pos, speed) 

        # random number constraint
        self.limit = self.image.get_height()


    def update(self, time_pass_sec):
        '''Move the sprite to a new position.
        
        Arguments:
        time_pass_sec -- updated time since last movement in seconds
        '''
        AnimSprite.update(self, time_pass_sec)

        # update the sprite's position
        self.rect.move_ip(self.distance_moved, 0)

        # if the sprite is out of screen update its place
        # to a new random (but still within the screen)        
        if self.rect.left >= self.area.right:
            self.rect.left = self.area.left - self.area.right
            self.rect.top = randint(self.area.top + self.limit,
                                    self.area.bottom - self.limit)

class SpriteSpeedError(ValueError):
    '''Raised when a non-acceptable sprite speed is set.'''

class SpriteTypeError(ValueError):
    '''Raised when a non-acceptable sprite type is set.'''

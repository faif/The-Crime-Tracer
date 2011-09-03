# -*- coding: utf-8 -*-

#    Sprite Movement, Animation Utilities.
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


try:
    import random
    import pygame
    import math
    import graphics

    from base import Base
    from generic_exceptions import *
    from vector import Vector2D
except (RuntimeError, ImportError) as error:
    import os, constants
    path = os.path.basename(__file__)
    print('{0}: {1}'.format(path, error))
    exit(constants.MOD_FAIL_ERR)


__all__ = [
            'Hipparchus',
            'Cardinal',
            'StaticSprite',
            'DynamicSprite',
            'SpriteFactory'
          ]


class Hipparchus(Base):
    MinimumDegree = 0
    MaximumDegree = 360

    def __init__(self): pass

    def getMinimumDegree(self):
        return Hipparchus.MinimumDegree

    def getMaximumDegree(self):
        return Hipparchus.MaximumDegree

    def getRadiansByDegrees(self, degrees):
        if isinstance(degrees, str):
            if degrees == 'Random':
                return random.randint(Hipparchus.MinimumDegree, Hipparchus.MaximumDegree)

        if isinstance(degrees, int):
            if degrees >= Hipparchus.MinimumDegree and degrees <= Hipparchus.MaximumDegree:
                return math.radians(degrees)

        raise FaultArgumentException("Incorrect Hipparchus Degree: {0}".format(degrees))


class Cardinal(Base):
    Mapping = {
        'North': (0, -1),
        'East':  (+1, 0),
        'South': (0, +1),
        'West':  (-1, 0),

        'NorthWest': (-0.707, -0.707),
        'NorthEast': (+0.707, -0.707),
        'SouthEast': (+0.707, +0.707),
        'SouthWest': (-0.707, +0.707)
    }

    def __init__(self): pass

    def getUnitVectorByDirection(self, direction):
        if isinstance(direction, str):
            if direction == 'Random':
                return Cardinal.Mapping[random.choice(Cardinal.Mapping.keys())]
            elif Cardinal.Mapping.has_key(direction):
                return Cardinal.Mapping[direction]

        raise FaultArgumentException("Incorrect Cardinal Direction: {0}".format(direction))

    def getDirectionByUnitVector(self, vector):
        if isinstance(vector, str):
            if vector == 'Random':
                return random.choice(Cardinal.Mapping.keys())

        if isinstance(vector, tuple) or isinstance(vector, list):
            for key, value in Cardinal.Mapping.items():
                if tuple(value) == tuple(vector):
                    return key

        raise FaultArgumentException("Incorrect Cardinal Unit Vector: {0}".format(vector))


class StaticSprite(pygame.sprite.Sprite, Base):
    def __init__(self, image, position, layer):
        pygame.sprite.Sprite.__init__(self)

        self.setImage(image)
        self.setPosition(position)
        self.setLayer(layer)
        self.arrangeRectangle()

    def setImage(self, image):
        self.image = graphics.load_image(image)[0]

    def setPosition(self, position):
        self.position = Vector2D(position)

    def setLayer(self, layer):
        self._layer = layer

        for group in self.groups():
            group.change_layer(self, layer)

    def arrangeRectangle(self):
        self.rect = self.image.get_rect(center=tuple(self.position))


class DynamicSprite(StaticSprite):
    def __init__(self, image, position, layer, speed):
        StaticSprite.__init__(self, image, position, layer)

        self.distance = 0.0
        self.setSpeed(speed)

    def setSpeed(self, speed):
        self.speed = speed

    def update(self, interval):
        self.distance = interval * self.speed


class CardinalSprite(DynamicSprite):
    def __init__(self, image, position, layer, speed, direction):
        DynamicSprite.__init__(self, image, position, layer, speed)

        self.setDirection(direction)

    def setDirection(self, direction):
        self.direction = Vector2D(Cardinal().getUnitVectorByDirection(direction))

    def update(self, interval):
        DynamicSprite.update(self, interval)

        self.position += self.direction * self.distance

        self.arrangeRectangle()


class InsistenceSprite(CardinalSprite):
    def __init__(self, image, position, layer, speed, direction):
        CardinalSprite.__init__(self, image, position, layer, speed, direction)

        self.original_direction = direction

    def update(self, interval):
        self.direction = Vector2D(Cardinal().getUnitVectorByDirection(self.original_direction))

        CardinalSprite.update(self, interval)


class HipparchusSprite(DynamicSprite):
    def __init__(self, image, position, layer, speed, angle):
        DynamicSprite.__init__(self, image, position, layer, speed)

        self.setAngle(angle)

    def setAngle(self, angle):
        self.angle = Hipparchus().getRadiansByDegrees(angle)
        
    def update(self, interval):
        DynamicSprite.update(self, interval)

        dx = math.sin(self.angle)
        dy = math.cos(self.angle)

        vector = Vector2D (dx, dy)

        self.position += vector * self.distance

        self.arrangeRectangle()


class SpriteFactory(Base):
    Sprites = {
        'Cardinal': CardinalSprite,
        'Insistence': InsistenceSprite,
        'Hipparchus': HipparchusSprite
    }

    def getSprite(self, type, image, position, layer, speed, direction):
        if SpriteFactory.Sprites.has_key(type):
            return SpriteFactory.Sprites[type](image, position, layer, speed, direction)
        else:
            raise FaultArgumentException("Incorrect Sprite Type: {0}".format(type))

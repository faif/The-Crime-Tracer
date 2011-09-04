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
            'StaticSprite',
            'DynamicSprite',
            'SpriteFactory'
          ]


class MinimumMaximum(Base):
   def __init__(self, minimum, maximum):
       if type(minimum) != type(maximum):
           raise FaultArgumentException("Minimum ({0}) is different than Maximum ({1})".format(type(minimum), type(maximum)))

       if minimum > maximum:
           raise FaultArgumentException("Minimum ({0}) must be less than Maximum ({1})".format(minimum, maximum))

       self.minimum = minimum
       self.maximum = maximum

   def getMinimum(self):
       return self.minimum

   def getMaximum(self):
       return self.maximum


class ValueLimitator(MinimumMaximum):
    def __init__(self, minimum, maximum):
        MinimumMaximum.__init__(self, minimum, maximum)

    def constrain(self, value):
        if value >= self.getMinimum() and value <= self.getMaximum():
            return value

        raise FaultArgumentException("Value ({0}) is out of range: [{1}, {2}]".format(value, self.getMinimum(), self.getMaximum()))


class IntegerLimitator(ValueLimitator):
    def __init__(self, minimum, maximum):
        ValueLimitator.__init__(self, minimum, maximum)

    def constrain (self, value):
        if isinstance(value, int):
            return ValueLimitator.constrain(self, value)

        if isinstance(value, str):
            if value == 'Random':
                return random.randint(self.getMinimum(), self.getMaximum())

        raise FaultArgumentException("Incorrect integer value: {0}".format(value))


class FloatLimitator(ValueLimitator):
    def __init__(self, minimum, maximum):
        ValueLimitator.__init__(self, minimum, maximum)

    def constrain (self, value):
        if isinstance(value, float):
            return ValueLimitator.constrain(self, value)

        if isinstance(value, str):
            if value == 'Random':
                return random.uniform(self.getMinimum(), self.getMaximum())

        raise FaultArgumentException("Incorrect float value: {0}".format(value))


class LimitatorFactory(Base):
    Limitators = {
        'Integer': IntegerLimitator,
        'Float': FloatLimitator
    }

    def getLimitator(self, type, minimum, maximum):
        if LimitatorFactory.Limitators.has_key(type):
            return LimitatorFactory.Limitators[type](minimum, maximum)
        else:
            raise FaultArgumentException("Incorrect limitator type: {0}".format(type))


class SpriteSpeed(Base):
    MinimumSpeed = 0
    MaximumSpeed = 1000

    def __init__(self):
        self.limitator = LimitatorFactory().getLimitator('Float', SpriteSpeed.MinimumSpeed, SpriteSpeed.MaximumSpeed)

    def getSpeed(self, speed):
        if isinstance (speed, int):
            speed = float (speed)

        return self.limitator.constrain(speed)


class SpriteAlpha(Base):
    MinimumAlpha = 0
    MaximumAlpha = 255

    def __init__(self):
        self.limitator = LimitatorFactory().getLimitator('Integer', SpriteAlpha.MinimumAlpha, SpriteAlpha.MaximumAlpha)

    def getAlpha(self, alpha):
        return self.limitator.constrain(alpha)


class SpriteAngle(Base):
    MinimumAngle = 0
    MaximumAngle = 360

    def __init__(self):
        self.limitator = LimitatorFactory().getLimitator('Float', SpriteAngle.MinimumAngle, SpriteAngle.MaximumAngle)

    def getAngle(self, angle):
        if isinstance (angle, int):
            angle = float (angle)

        return self.limitator.constrain(angle)


class SpriteLayer(Base):
    MinimumLayer = 0
    MaximumLayer = 200

    def __init__(self):
        self.limitator = LimitatorFactory().getLimitator('Integer', SpriteLayer.MinimumLayer, SpriteLayer.MaximumLayer)

    def getLayer(self, layer):
        return self.limitator.constrain(layer)


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

        raise FaultArgumentException("Incorrect Cardinal direction: {0}".format(direction))

    def getDirectionByUnitVector(self, vector):
        if isinstance(vector, str):
            if vector == 'Random':
                return random.choice(Cardinal.Mapping.keys())

        if isinstance(vector, tuple) or isinstance(vector, list):
            for key, value in Cardinal.Mapping.items():
                if tuple(value) == tuple(vector):
                    return key

        raise FaultArgumentException("Incorrect Cardinal unit vector: {0}".format(vector))


class StaticSprite(pygame.sprite.Sprite, Base):
    def __init__(self, image, position, layer, alpha):
        pygame.sprite.Sprite.__init__(self)

        self.setImage(image)
        self.setPosition(position)
        self.setLayer(layer)
        self.setAlpha(alpha)
        self.arrangeRectangle()

    def setImage(self, image):
        self.image = graphics.load_image(image)[0]

    def setPosition(self, position):
        self.position = Vector2D(position)

    def setLayer(self, layer):
        layer = SpriteLayer().getLayer(layer)

        self._layer = layer

        for group in self.groups():
            group.change_layer(self, layer)

    def setAlpha(self, alpha):
        self.image.set_alpha(SpriteAlpha().getAlpha(alpha))

    def arrangeRectangle(self):
        self.rect = self.image.get_rect(center=tuple(self.position))


class DynamicSprite(StaticSprite):
    def __init__(self, image, position, layer, alpha, speed):
        StaticSprite.__init__(self, image, position, layer, alpha)

        self.distance = 0.0
        self.setSpeed(speed)

    def setSpeed(self, speed):
        self.speed = SpriteSpeed().getSpeed(speed)

    def update(self, interval):
        self.distance = interval * self.speed


class CardinalSprite(DynamicSprite):
    def __init__(self, image, position, layer, alpha, speed, direction):
        DynamicSprite.__init__(self, image, position, layer, alpha, speed)

        self.setDirection(direction)

    def setDirection(self, direction):
        self.direction = Vector2D(Cardinal().getUnitVectorByDirection(direction))

    def update(self, interval):
        DynamicSprite.update(self, interval)

        self.position += self.direction * self.distance

        self.arrangeRectangle()


class InsistenceSprite(CardinalSprite):
    def __init__(self, image, position, layer, alpha, speed, direction):
        CardinalSprite.__init__(self, image, position, layer, alpha, speed, direction)

        self.original_direction = direction

    def update(self, interval):
        self.direction = Vector2D(Cardinal().getUnitVectorByDirection(self.original_direction))

        CardinalSprite.update(self, interval)


class HipparchusSprite(DynamicSprite):
    def __init__(self, image, position, layer, alpha, speed, angle):
        DynamicSprite.__init__(self, image, position, layer, alpha, speed)

        self.setAngle(angle)

    def setAngle(self, angle):
        self.angle = math.radians(SpriteAngle().getAngle(angle))
        
    def update(self, interval):
        DynamicSprite.update(self, interval)

        dy = math.sin(self.angle)
        dx = math.cos(self.angle)

        vector = Vector2D (dx, dy)

        self.position += vector * self.distance

        self.arrangeRectangle()


class SpriteFactory(Base):
    Sprites = {
        'Cardinal': CardinalSprite,
        'Insistence': InsistenceSprite,
        'Hipparchus': HipparchusSprite
    }

    def getSprite(self, type, image, position, layer, alpha, speed, direction):
        if SpriteFactory.Sprites.has_key(type):
            return SpriteFactory.Sprites[type](image, position, layer, alpha, speed, direction)
        else:
            raise FaultArgumentException("Incorrect sprite type: {0}".format(type))

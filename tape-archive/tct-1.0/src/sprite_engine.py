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
    def __init__(self, type, minimum, maximum):
        if not isinstance(minimum, type):
            raise FaultArgumentException("Minimum type should be: {0}".format(type))

        if not isinstance(maximum, type):
            raise FaultArgumentException("Maximum type should be: {0}".format(type))

        if minimum > maximum:
            raise FaultArgumentException("Minimum ({0}) must be less than Maximum ({1})".format(minimum, maximum))

        self.minimum = minimum
        self.maximum = maximum

        self.type = type

    def getMinimum(self):
        return self.minimum

    def getMaximum(self):
        return self.maximum


class ValueBounder(MinimumMaximum):
    def __init__(self, type, minimum, maximum):
        super(ValueBounder, self).__init__(type, minimum, maximum)

    def constrain(self, value):
        if isinstance(value, self.type):
            if value >= self.getMinimum() and value <= self.getMaximum():
                return value
            else:
                raise FaultArgumentException("Value ({0}) is out of range: [{1}, {2}]".format(value, self.getMinimum(), self.getMaximum()))
        else:
            raise FaultArgumentException("Type of value should be: {0}".format(self.type))


class IntegerBounder(ValueBounder):
    def __init__(self, minimum, maximum):
        super(IntegerBounder, self).__init__(int, minimum, maximum)

    def constrain (self, value):
        if isinstance(value, str):
            if value == 'Random':
                return random.randint(self.getMinimum(), self.getMaximum())

        return super(IntegerBounder, self).constrain(value)


class FloatBounder(ValueBounder):
    def __init__(self, minimum, maximum):
        super(FloatBounder, self).__init__(float, minimum, maximum)

    def constrain (self, value):
        if isinstance(value, str):
            if value == 'Random':
                return random.uniform(self.getMinimum(), self.getMaximum())

        return super(FloatBounder, self).constrain(value)


class BounderFactory(Base):
    Bounders = {
        'Integer': IntegerBounder, 'Float': FloatBounder
    }

    def getBounder(self, type, minimum, maximum):
        if BounderFactory.Bounders.has_key(type):
            return BounderFactory.Bounders[type](minimum, maximum)
        else:
            raise FaultArgumentException("Incorrect bounder type: {0}".format(type))


class SpriteSpeed(Base):
    MinimumSpeed = 0.0
    MaximumSpeed = 1000.0

    def __init__(self):
        self.bounder = BounderFactory().getBounder('Float', SpriteSpeed.MinimumSpeed, SpriteSpeed.MaximumSpeed)

    def getSpeed(self, speed):
        if isinstance (speed, int):
            speed = float (speed)

        return self.bounder.constrain(speed)


class SpriteAlpha(Base):
    MinimumAlpha = 0
    MaximumAlpha = 255

    def __init__(self):
        self.bounder = BounderFactory().getBounder('Integer', SpriteAlpha.MinimumAlpha, SpriteAlpha.MaximumAlpha)

    def getAlpha(self, alpha):
        return self.bounder.constrain(alpha)


class SpriteAngle(Base):
    MinimumAngle = 0.0
    MaximumAngle = 360.0

    def __init__(self):
        self.bounder = BounderFactory().getBounder('Float', SpriteAngle.MinimumAngle, SpriteAngle.MaximumAngle)

    def getAngle(self, angle):
        if isinstance (angle, int):
            angle = float (angle)

        return self.bounder.constrain(angle)


class SpriteLayer(Base):
    MinimumLayer = 0
    MaximumLayer = 200

    def __init__(self):
        self.bounder = BounderFactory().getBounder('Integer', SpriteLayer.MinimumLayer, SpriteLayer.MaximumLayer)

    def getLayer(self, layer):
        return self.bounder.constrain(layer)


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


class SpriteLimiter:
    def run(self, sprite):
        pass


class MirrorLimiter(SpriteLimiter):
    def run(self, sprite):
        if sprite.rect.top > sprite.area.bottom:
            sprite.rect.bottom = sprite.area.top
            sprite.arrangePosition()
        elif sprite.rect.bottom < sprite.area.top:
            sprite.rect.top = sprite.area.bottom
            sprite.arrangePosition()
        elif sprite.rect.left > sprite.area.right:
            sprite.rect.right = sprite.area.left
            sprite.arrangePosition()
        elif sprite.rect.right < sprite.area.left:
            sprite.rect.left = sprite.area.right
            sprite.arrangePosition()


class LimiterFactory(Base):
    Limiters = {
        'Mirror': MirrorLimiter
    }

    def getLimiter(self, type):
        if LimiterFactory.Limiters.has_key(type):
            return LimiterFactory.Limiters[type]()
        else:
            raise FaultArgumentException("Incorrect limiter type: {0}".format(type))


class StaticSprite(pygame.sprite.Sprite, Base):
    def __init__(self, image, position, layer, alpha):
        super(StaticSprite, self).__init__()

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

    def arrangePosition(self):
        self.position = Vector2D(self.rect.center)


class DynamicSprite(StaticSprite):
    def __init__(self, image, position, layer, alpha, speed, area):
        super(DynamicSprite, self).__init__(image, position, layer, alpha)

        self.distance = 0.0

        self.setSpeed(speed)
        self.setArea(area)

        self.limiter = LimiterFactory().getLimiter('Mirror')

    def setSpeed(self, speed):
        self.speed = SpriteSpeed().getSpeed(speed)

    def setArea(self, area):
        self.area = area

    def setLimiter(self, limiter):
        self.limiter = LimiterFactory().getLimiter(limiter)

    def update(self, interval):
        self.distance = interval * self.speed


class CardinalSprite(DynamicSprite):
    def __init__(self, image, position, layer, alpha, speed, area, direction):
        super(CardinalSprite, self).__init__(image, position, layer, alpha, speed, area)

        self.setDirection(direction)

    def setDirection(self, direction):
        self.direction = Vector2D(Cardinal().getUnitVectorByDirection(direction))

    def update(self, interval):
        super(CardinalSprite, self).update(interval)

        self.position += self.direction * self.distance

        self.arrangeRectangle()

        self.limiter.run(self)


class InsistenceSprite(CardinalSprite):
    def __init__(self, image, position, layer, alpha, speed, area, direction):
        super(InsistenceSprite, self).__init__(image, position, layer, alpha, speed, area, direction)

        self.original_direction = direction

    def update(self, interval):
        self.direction = Vector2D(Cardinal().getUnitVectorByDirection(self.original_direction))

        super(InsistenceSprite, self).update(interval)


class HipparchusSprite(DynamicSprite):
    def __init__(self, image, position, layer, alpha, speed, area, angle):
        super(HipparchusSprite, self).__init__(image, position, layer, alpha, speed, area)

        self.setAngle(angle)

    def setAngle(self, angle):
        self.angle = math.radians(SpriteAngle().getAngle(angle))
        
    def update(self, interval):
        super(HipparchusSprite, self).update(interval)

        dy = math.sin(self.angle)
        dx = math.cos(self.angle)

        vector = Vector2D (dx, dy)

        self.position += vector * self.distance

        self.arrangeRectangle()

        self.limiter.run(self)


class SpriteFactory(Base):
    Sprites = {
        'Cardinal': CardinalSprite,
        'Insistence': InsistenceSprite,
        'Hipparchus': HipparchusSprite
    }

    def getSprite(self, type, image, position, layer, alpha, speed, area, direction):
        if SpriteFactory.Sprites.has_key(type):
            return SpriteFactory.Sprites[type](image, position, layer, alpha, speed, area, direction)
        else:
            raise FaultArgumentException("Incorrect sprite type: {0}".format(type))

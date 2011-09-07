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
    import math
    import random
    import pygame
    import graphics

    from base import Base
    from borg import Borg

    from gameobjects.vector2 import Vector2
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
            raise ValueError("Minimum type should be: {0}".format(type))

        if not isinstance(maximum, type):
            raise ValueError("Maximum type should be: {0}".format(type))

        if minimum > maximum:
            raise ValueError("Minimum ({0}) must be less than Maximum ({1})".format(minimum, maximum))

        self._minimum = minimum
        self._maximum = maximum

        self._type = type

    @property
    def minimum(self):
        return self._minimum

    @property
    def maximum(self):
        return self._maximum

    @property
    def type(self):
        return self._type


class ValueBounder(MinimumMaximum):
    def __init__(self, type, minimum, maximum):
        super(ValueBounder, self).__init__(type, minimum, maximum)

    def constrain(self, value):
        if isinstance(value, self.type):
            if value >= self.minimum and value <= self.maximum:
                return value
            else:
                raise ValueError("Value ({0}) is out of range: [{1}, {2}]".format(value, self.minimum, self.maximum))
        else:
            raise ValueError("Type of value should be: {0}".format(self.type))


class IntegerBounder(ValueBounder):
    def __init__(self, minimum, maximum):
        super(IntegerBounder, self).__init__(int, minimum, maximum)

    def constrain (self, value):
        if isinstance(value, str):
            if value == 'Random':
                return random.randint(self.minimum, self.maximum)

        return super(IntegerBounder, self).constrain(value)


class FloatingBounder(ValueBounder):
    def __init__(self, minimum, maximum):
        super(FloatingBounder, self).__init__(float, minimum, maximum)

    def constrain (self, value):
        if isinstance(value, str):
            if value == 'Random':
                return random.uniform(self.minimum, self.maximum)

        return super(FloatingBounder, self).constrain(value)


class BounderFactory(Borg):
    __bounders = {
        'Integer': IntegerBounder,
        'Floating': FloatingBounder
    }

    def __init__(self):
        super(BounderFactory, self).__init__()

    def getBounder(self, type, minimum, maximum):
        if BounderFactory.__bounders.has_key(type):
            return BounderFactory.__bounders[type](minimum, maximum)
        else:
            raise ValueError("Incorrect bounder type: {0}".format(type))


class SpriteSpeed(Borg):
    __minimumSpeed = 0.0
    __maximumSpeed = 1000.0

    __bounder = BounderFactory().getBounder('Floating', __minimumSpeed, __maximumSpeed)

    def __init__(self):
        super(SpriteSpeed, self).__init__()

    def constrain(self, speed):
        if isinstance (speed, int):
            speed = float (speed)

        return SpriteSpeed.__bounder.constrain(speed)


class SpriteAlpha(Borg):
    __minimumAlpha = 0
    __maximumAlpha = 255

    __bounder = BounderFactory().getBounder('Integer', __minimumAlpha, __maximumAlpha)

    def __init__(self):
        super(SpriteAlpha, self).__init__()

    def constrain(self, alpha):
        return SpriteAlpha.__bounder.constrain(alpha)


class SpriteAngle(Borg):
    __minimumAngle = 0.0
    __maximumAngle = 360.0

    __bounder = BounderFactory().getBounder('Floating', __minimumAngle, __maximumAngle)

    def __init__(self):
        super(SpriteAngle, self).__init__()

    def constrain(self, angle):
        if isinstance (angle, int):
            angle = float (angle)

        return SpriteAngle.__bounder.constrain(angle)


class SpriteLayer(Borg):
    __minimumLayer = 0
    __maximumLayer = 200

    __bounder = BounderFactory().getBounder('Integer', __minimumLayer, __maximumLayer)

    def __init__(self):
        super(SpriteLayer, self).__init__()

    def constrain(self, layer):
        return SpriteLayer.__bounder.constrain(layer)


class Cardinal(Borg):
    __mapping = {
        'North': (0, -1),
        'East':  (+1, 0),
        'South': (0, +1),
        'West':  (-1, 0),

        'NorthWest': (-0.707, -0.707),
        'NorthEast': (+0.707, -0.707),
        'SouthEast': (+0.707, +0.707),
        'SouthWest': (-0.707, +0.707)
    }

    def __init__(self):
        super(Cardinal, self).__init__()

    def getUnitVectorByDirection(self, direction):
        if isinstance(direction, str):
            if direction == 'Random':
                return Cardinal.__mapping[random.choice(Cardinal.__mapping.keys())]
            elif Cardinal.__mapping.has_key(direction):
                return Cardinal.__mapping[direction]

        raise ValueError("Incorrect Cardinal direction: {0}".format(direction))

    def getDirectionByUnitVector(self, vector):
        if isinstance(vector, str):
            if vector == 'Random':
                return random.choice(Cardinal.__mapping.keys())

        if isinstance(vector, tuple) or isinstance(vector, list):
            for key, value in Cardinal.__mapping.items():
                if tuple(value) == tuple(vector):
                    return key

        raise ValueError("Incorrect Cardinal unit vector: {0}".format(vector))


class SpriteLimiter(Base):
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


class LimiterFactory(Borg):
    __limiters = {
        'Mirror': MirrorLimiter
    }

    def __init__(self):
        super(LimiterFactory, self).__init__()

    def getLimiter(self, type):
        if LimiterFactory.__limiters.has_key(type):
            return LimiterFactory.__limiters[type]()
        else:
            raise ValueError("Incorrect limiter type: {0}".format(type))


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
        self.position = Vector2(position)

    def setLayer(self, layer):
        layer = SpriteLayer().constrain(layer)

        self._layer = layer

        for group in self.groups():
            group.change_layer(self, layer)

    def setAlpha(self, alpha):
        self.image.set_alpha(SpriteAlpha().constrain(alpha))

    def arrangeRectangle(self):
        self.rect = self.image.get_rect(center=tuple(self.position))

    def arrangePosition(self):
        self.position = Vector2(self.rect.center)


class DynamicSprite(StaticSprite):
    def __init__(self, image, position, layer, alpha, speed, area):
        super(DynamicSprite, self).__init__(image, position, layer, alpha)

        self.distance = 0.0

        self.setSpeed(speed)
        self.setArea(area)

        self.limiter = LimiterFactory().getLimiter('Mirror')

    def setSpeed(self, speed):
        self.speed = SpriteSpeed().constrain(speed)

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
        self.direction = Vector2(Cardinal().getUnitVectorByDirection(direction))

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
        self.direction = Vector2(Cardinal().getUnitVectorByDirection(self.original_direction))

        super(InsistenceSprite, self).update(interval)


class HipparchusSprite(DynamicSprite):
    def __init__(self, image, position, layer, alpha, speed, area, angle):
        super(HipparchusSprite, self).__init__(image, position, layer, alpha, speed, area)

        self.setAngle(angle)

    def setAngle(self, angle):
        self.angle = math.radians(SpriteAngle().constrain(angle))
        
    def update(self, interval):
        super(HipparchusSprite, self).update(interval)

        dy = math.sin(self.angle)
        dx = math.cos(self.angle)

        vector = Vector2(dx, dy)

        self.position += vector * self.distance

        self.arrangeRectangle()

        self.limiter.run(self)


class SpriteFactory(Borg):
    __sprites = {
        'Cardinal': CardinalSprite,
        'Insistence': InsistenceSprite,
        'Hipparchus': HipparchusSprite
    }

    def __init__(self):
        super(SpriteFactory, self).__init__()

    def getSprite(self, type, image, position, layer, alpha, speed, area, direction):
        if SpriteFactory.__sprites.has_key(type):
            return SpriteFactory.__sprites[type](image, position, layer, alpha, speed, area, direction)
        else:
            raise ValueError("Incorrect sprite type: {0}".format(type))

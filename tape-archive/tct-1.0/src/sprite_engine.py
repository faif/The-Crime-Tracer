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

        self.__minimum = minimum
        self.__maximum = maximum

        self.__type = type

    @property
    def minimum(self):
        return self.__minimum

    @property
    def maximum(self):
        return self.__maximum

    @property
    def type(self):
        return self.__type


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
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    def run(self, sprite):
        pass


class DefaultLimiter(SpriteLimiter):
    def __init__(self, name):
        super(DefaultLimiter, self).__init__(name)

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
        'Default': DefaultLimiter
    }

    def __init__(self):
        super(LimiterFactory, self).__init__()

    def getLimiter(self, type):
        if LimiterFactory.__limiters.has_key(type):
            return LimiterFactory.__limiters[type](type)
        else:
            raise ValueError("Incorrect limiter type: {0}".format(type))


class StaticSprite(pygame.sprite.Sprite, Base):
    def __init__(self, file, position, layer, alpha):
        super(StaticSprite, self).__init__()

        self.file = file
        self.position = position
        self._layer = layer
        self.alpha = alpha

        self.arrangeRectangle()

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, file):
        self.image = self._file = file

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image):
        self._image = graphics.load_image(image)[0]

    @property
    def position(self):
        return tuple(self._position)

    @position.setter
    def position(self, position):
        self._position = Vector2(position)

    @property
    def _layer(self):
        return self.layer

    @_layer.setter
    def _layer(self, layer):
        self.layer = SpriteLayer().constrain(layer)
        for group in self.groups():
            group.change_layer(self, self.layer)

    @property
    def alpha(self):
        return self._image.get_alpha()

    @alpha.setter
    def alpha(self, alpha):
        self._image.set_alpha(SpriteAlpha().constrain(alpha))

    @property
    def rect(self):
        return self._rect

    def arrangeRectangle(self):
        self._rect = self._image.get_rect(center=tuple(self._position))

    def arrangePosition(self):
        self._position = Vector2(self._rect.center)


class DynamicSprite(StaticSprite):
    def __init__(self, file, position, layer, alpha, speed, area):
        super(DynamicSprite, self).__init__(file, position, layer, alpha)

        self._distance = 0.0

        self.speed = speed
        self.area = area

        self.limiter = 'Default'

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed):
        self._speed = SpriteSpeed().constrain(speed)

    @property
    def area(self):
        return self._area

    @area.setter
    def area(self, area):
        self._area = area

    @property
    def limiter(self):
        return self._limiter.name

    @limiter.setter
    def limiter(self, limiter):
        self._limiter = LimiterFactory().getLimiter(limiter)

    def update(self, interval):
        self._distance = interval * self._speed


class CardinalSprite(DynamicSprite):
    def __init__(self, file, position, layer, alpha, speed, area, direction):
        super(CardinalSprite, self).__init__(file, position, layer, alpha, speed, area)

        self.direction = direction

    @property
    def direction(self):
        return Cardinal().getDirectionByUnitVector(tuple(self._direction))

    @direction.setter
    def direction(self, direction):
        self._direction = Vector2(Cardinal().getUnitVectorByDirection(direction))

    def update(self, interval):
        super(CardinalSprite, self).update(interval)

        self._position += self._direction * self._distance

        self.arrangeRectangle()

        self._limiter.run(self)


class InsistenceSprite(CardinalSprite):
    def __init__(self, file, position, layer, alpha, speed, area, direction):
        super(InsistenceSprite, self).__init__(file, position, layer, alpha, speed, area, direction)

        self.original = direction

    @property
    def original(self):
        return self._original

    @original.setter
    def original(self, original):
        self._original = original

    def update(self, interval):
        self.direction = self.original

        super(InsistenceSprite, self).update(interval)


class HipparchusSprite(DynamicSprite):
    def __init__(self, file, position, layer, alpha, speed, area, angle):
        super(HipparchusSprite, self).__init__(file, position, layer, alpha, speed, area)

        self.angle = angle

    @property
    def angle(self):
        return math.degrees(self._angle)

    @angle.setter
    def angle(self, angle):
        self._angle = math.radians(SpriteAngle().constrain(angle))

    def update(self, interval):
        super(HipparchusSprite, self).update(interval)

        dy = math.sin(self._angle)
        dx = math.cos(self._angle)

        vector = Vector2(dx, dy)

        self._position += vector * self._distance

        self.arrangeRectangle()

        self._limiter.run(self)


class SpriteFactory(Borg):
    __sprites = {
        'Cardinal': CardinalSprite,
        'Insistence': InsistenceSprite,
        'Hipparchus': HipparchusSprite
    }

    def __init__(self):
        super(SpriteFactory, self).__init__()

    def getSprite(self, type, file, position, layer, alpha, speed, area, direction):
        if SpriteFactory.__sprites.has_key(type):
            return SpriteFactory.__sprites[type](file, position, layer, alpha, speed, area, direction)
        else:
            raise ValueError("Incorrect sprite type: {0}".format(type))

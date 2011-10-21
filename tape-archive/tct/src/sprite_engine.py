# -*- coding: utf-8 -*-

#    Sprite Animation & Movement Engine.
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

    from borg import Borg

    from resource_manager import ResourceManager

    from gameobjects.vector2 import Vector2
except (RuntimeError, ImportError) as error:
    import os, constants
    path = os.path.basename(__file__)
    print('{0}: {1}'.format(path, error))
    exit(constants.MOD_FAIL_ERR)


__all__ = [
            'StaticSprite',
            'DynamicSprite',

            'TravelSprite',
            'CardinalSprite',
            'ShakingSprite',
            'HipparchusSprite',

            'StaticAnimation',

            'AreaLimiter',
            'LimiterFactory'
          ]


class MinimumMaximum(object):
    def __init__(self, type, minimum, maximum):
        if not isinstance(minimum, type):
            raise ValueError("Minimum value ({0}) should be type of ({1})".format(minimum, type))

        if not isinstance(maximum, type):
            raise ValueError("Maximum value ({0}) should be type of ({1})".format(maximum, type))

        if minimum > maximum:
            raise ValueError("Minimum value ({0}) must be less than Maximum value ({1})".format(minimum, maximum))

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

    def check(self, value):
        if isinstance(value, self.type):
            if value >= self.minimum and value <= self.maximum:
                return value
            else:
                raise ValueError("Value ({0}) is out of range [ {1}, {2} ]".format(value, self.minimum, self.maximum))
        else:
            raise ValueError("Value ({0}) should be type of ({1})".format(value, self.type))


class IntegerFilter(ValueBounder):
    def __init__(self, minimum, maximum):
        super(IntegerFilter, self).__init__(int, minimum, maximum)

    def check (self, value):
        if isinstance(value, str):
            if value == 'Random':
                return random.randint(self.minimum, self.maximum)

        return super(IntegerFilter, self).check(value)


class FloatingFilter(ValueBounder):
    def __init__(self, minimum, maximum):
        super(FloatingFilter, self).__init__(float, minimum, maximum)

    def check (self, value):
        if isinstance(value, str):
            if value == 'Random':
                return random.uniform(self.minimum, self.maximum)

        return super(FloatingFilter, self).check(value)


class FilterFactory(Borg):
    __filters = {
        'Integer': IntegerFilter,
        'Floating': FloatingFilter
    }

    def __init__(self):
        super(FilterFactory, self).__init__()

    def getInstance(self, type, minimum, maximum):
        if FilterFactory.__filters.has_key(type):
            return FilterFactory.__filters[type](minimum, maximum)
        else:
            raise ValueError("Incorrect filter type ({0})".format(type))


class SpeedHandler(Borg):
    __minimum, __maximum = 0.0, 1000.0

    __filter = FilterFactory().getInstance('Floating', __minimum, __maximum)

    def __init__(self):
        super(SpeedHandler, self).__init__()

    def handle(self, speed):
        if isinstance (speed, int):
            speed = float (speed)

        return SpeedHandler.__filter.check(speed)


class AlphaHandler(Borg):
    __minimum, __maximum = 0, 255

    __filter = FilterFactory().getInstance('Integer', __minimum, __maximum)

    def __init__(self):
        super(AlphaHandler, self).__init__()

    def handle(self, alpha):
        return AlphaHandler.__filter.check(alpha)


class AngleHandler(Borg):
    __minimum, __maximum = 0.0, 360.0

    __filter = FilterFactory().getInstance('Floating', __minimum, __maximum)

    def __init__(self):
        super(AngleHandler, self).__init__()

    def handle(self, angle):
        if isinstance (angle, int):
            angle = float (angle)

        return AngleHandler.__filter.check(angle)


class LayerHandler(Borg):
    __minimum, __maximum = 0, 200

    __filter = FilterFactory().getInstance('Integer', __minimum, __maximum)

    def __init__(self):
        super(LayerHandler, self).__init__()

    def handle(self, layer):
        return LayerHandler.__filter.check(layer)


class SizeHandler(Borg):
    __minimum, __maximum = 1, 1000

    __filter = FilterFactory().getInstance('Integer', __minimum, __maximum)

    def __init__(self):
        super(SizeHandler, self).__init__()

    def handle(self, size):
        return SizeHandler.__filter.check(size)


class FPSHandler(Borg):
    __minimum, __maximum = 1, 100

    __filter = FilterFactory().getInstance('Integer', __minimum, __maximum)

    def __init__(self):
        super(FPSHandler, self).__init__()

    def handle(self, fps):
        return FPSHandler.__filter.check(fps)


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

        raise ValueError("Incorrect Cardinal direction ({0})".format(direction))

    def getDirectionByUnitVector(self, vector):
        if isinstance(vector, str):
            if vector == 'Random':
                return random.choice(Cardinal.__mapping.keys())

        if isinstance(vector, tuple) or isinstance(vector, list):
            for key, value in Cardinal.__mapping.items():
                if tuple(value) == tuple(vector):
                    return key

        raise ValueError("Incorrect Cardinal unit vector ({0})".format(vector))


class AreaLimiter(object):
    def run(self, sprite):
        pass


class DefaultLimiter(AreaLimiter):
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

    def getInstance(self, type):
        if LimiterFactory.__limiters.has_key(type):
            return LimiterFactory.__limiters[type]()
        else:
            raise ValueError("Incorrect limiter type: {0}".format(type))


class StaticSprite(pygame.sprite.Sprite):
    def __init__(self, file, position, layer, alpha, reuse):
        super(StaticSprite, self).__init__()

        self.reuse = reuse
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
        self._image = ResourceManager().getImage(file, reuse = self._reuse)
        self._file = file

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
        self.layer = LayerHandler().handle(layer)
        for group in self.groups():
            group.change_layer(self, layer)

    @property
    def alpha(self):
        return self._image.get_alpha()

    @alpha.setter
    def alpha(self, alpha):
        self._image.set_alpha(AlphaHandler().handle(alpha))

    @property
    def reuse(self):
        return self._reuse

    @reuse.setter
    def reuse(self, reuse):
        self._reuse = reuse

    @property
    def image(self):
        return self._image

    @property
    def rect(self):
        return self._rect

    def arrangeRectangle(self):
        self._rect = self._image.get_rect(center=tuple(self._position))

    def arrangePosition(self):
        self._position = Vector2(self._rect.center)


class DynamicSprite(StaticSprite):
    def __init__(self, file, position, layer, alpha, reuse, speed, area):
        super(DynamicSprite, self).__init__(file, position, layer, alpha, reuse)

        self.limiter = None
        self.speed = speed
        self.area = area

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed):
        self._speed = SpeedHandler().handle(speed)

    @property
    def area(self):
        return self._area

    @area.setter
    def area(self, area):
        self._area = area

    @property
    def limiter(self):
        return self._limiter

    @limiter.setter
    def limiter(self, limiter):
        self._limiter = limiter

    def update(self, interval):
        self._distance = interval * self._speed


class TravelSprite(DynamicSprite):
    __arrivalThreshold = 8

    def __init__(self, file, position, layer, alpha, reuse, speed, area):
        super(TravelSprite, self).__init__(file, position, layer, alpha, reuse, speed, area)

        self.stop()

    @property
    def destination(self):
        return tuple(self._destination)

    @destination.setter
    def destination(self, destination):
        self._destination = Vector2(destination)

    def _forget(self):
        self._destination = self._position

    def _range(self):
        return self._heading().get_length()

    def _heading(self):
        return Vector2.from_points(self._position, self._destination)

    def move(self):
        self._travelling = True

    def still(self):
        self._travelling = False

    def travels(self):
        return self._travelling

    def stop(self):
        self._forget() ; self.still()

    def approach(self):
        self._position += self._heading().normalise() * self._distance

    def arrived(self):
        return self._range() < TravelSprite.__arrivalThreshold

    def update(self, interval):
        super(TravelSprite, self).update(interval)


class CardinalSprite(DynamicSprite):
    def __init__(self, file, position, layer, alpha, reuse, speed, area, direction):
        super(CardinalSprite, self).__init__(file, position, layer, alpha, reuse, speed, area)

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


class ShakingSprite(CardinalSprite):
    __original = 'Random'

    def __init__(self, file, position, layer, alpha, reuse, speed, area):
        super(ShakingSprite, self).__init__(file, position, layer, alpha, reuse, speed, area, ShakingSprite.__original)

    def update(self, interval):
        self.direction = ShakingSprite.__original

        super(ShakingSprite, self).update(interval)


class HipparchusSprite(DynamicSprite):
    def __init__(self, file, position, layer, alpha, reuse, speed, area, angle):
        super(HipparchusSprite, self).__init__(file, position, layer, alpha, reuse, speed, area)

        self.angle = angle

    @property
    def angle(self):
        return math.degrees(self._angle)

    @angle.setter
    def angle(self, angle):
        self._angle = math.radians(AngleHandler().handle(angle))

    def update(self, interval):
        super(HipparchusSprite, self).update(interval)

        dy = math.sin(self._angle)
        dx = math.cos(self._angle)

        heading = Vector2(dx, dy)

        self._position += heading * self._distance


class StaticAnimation(pygame.sprite.Sprite):
    def __init__(self, sheet, position, layer, alpha, reuse, width, height, fps):
        super(StaticAnimation, self).__init__()

        self.position = position
        self._layer = layer
        self.reuse = reuse

        self.useSpriteSheet(sheet, width, height, fps)

        self.alpha = alpha

        self.arrangeRectangle()

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
        self.layer = LayerHandler().handle(layer)
        for group in self.groups():
            group.change_layer(self, layer)

    @property
    def reuse(self):
        return self._reuse

    @reuse.setter
    def reuse(self, reuse):
        self._reuse = reuse

    @property
    def alpha(self):
        return self._image.get_alpha()

    @alpha.setter
    def alpha(self, alpha):
        alpha = AlphaHandler().handle(alpha)
        for image in self._images:
            image.set_alpha(alpha)

    @property
    def image(self):
        return self._image

    @property
    def rect(self):
        return self._rect

    def arrangeRectangle(self):
        self._rect = self._image.get_rect(center=tuple(self._position))

    def arrangePosition(self):
        self._position = Vector2(self._rect.center)

    def useSpriteSheet (self, sheet, width, height, fps):
        width = SizeHandler().handle(width)
        height = SizeHandler().handle(height)
        fps = FPSHandler().handle(fps)

        self._images = self._sliceSpriteSheet (sheet, width, height)

        self._delay = 1000 / fps
        self._last_update = 0
        self._frame = 0

        self._image = self._images[self._frame]

    def _sliceSpriteSheet (self, sheet, width, height):
        images = []

        masterImage = ResourceManager().getImage(sheet, self._reuse)

        masterWidth, masterHeight = masterImage.get_size ()

        for i in range (int (masterWidth / width)):
            images.append (masterImage.subsurface ((i * width, 0, width, height)))

        return images

    def update(self, interval):
        interval = pygame.time.get_ticks()

        if interval - self._last_update > self._delay:
            self._frame += 1

            if self._frame >= len(self._images):
                self._frame = 0
                self._last_update = 0

            self._image = self._images[self._frame]
            self._last_update = interval

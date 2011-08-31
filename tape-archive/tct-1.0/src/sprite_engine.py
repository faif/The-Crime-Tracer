import random
import pygame
import math

from graphics import load_image
from vector import Vector2D


class FaultArgumentError(ValueError):
    '''Raised when a fault argument is passed as parameter.'''


class Hipparchus(object):
    minDegree = 0
    maxDegree = 360

    def __init__(self): pass

    def getMinDegree(self):
        return Hipparchus.minDegree

    def getMaxDegree(self):
        return Hipparchus.maxDegree

    def getRadiansByDegrees(self, degrees):
        if isinstance(degrees, int):
            if degrees >= Hipparchus.minDegree and degrees <= Hipparchus.maxDegree:
                return math.radians(degrees)

        raise FaultArgumentError("Incorrect Hipparchus degree: {0}".format(degrees))



class Cardinal(object):
    mapping = {
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

    def getDirections(self):
        return Cardinal.mapping.keys()

    def getUnitVectors(self):
        return Cardinal.mapping.values()

    def getUnitVectorByDirection(self, direction):
        if isinstance(direction, str):
            if direction == "Random":
                return Cardinal.mapping[random.choice(Cardinal.mapping.keys())]
            elif Cardinal.mapping.has_key(direction):
                return Cardinal.mapping[direction]

        raise FaultArgumentError("Incorrect Cardinal direction: {0}".format(direction))

    def getDirectionByUnitVector(self, vector):
        if isinstance(vector, str):
            if vector == "Random":
                return random.choice(Cardinal.mapping.keys())

        if isinstance(vector, tuple) or isinstance(vector, list):
            for key, value in Cardinal.mapping.items():
                if list(value) == list(vector):
                    return key

        raise FaultArgumentError("Incorrect Cardinal unit vector: {0}".format(vector))


class StaticSprite(pygame.sprite.Sprite):
    def __init__(self, image, position, layer):
        pygame.sprite.Sprite.__init__(self)

        self.setImage(image)
        self.setPosition(position)
        self.setLayer(layer)
        self.centering()

    def setImage(self, image):
        self.image = load_image(image)[0]

    def setPosition(self, position):
        self.position = Vector2D(position)

    def setLayer(self, layer):
        self._layer = layer

    def setRect(self, rect):
        self.rect = rect

    def getImage(self):
        return self.image

    def getPosition(self):
        return self.position

    def getLayer(self):
        return self._layer

    def getRect(self):
        return self.rect

    def centering(self):
        self.rect = self.image.get_rect(center=list(self.position))


class DynamicSprite(StaticSprite):
    def __init__(self, image, position, layer, speed):
        StaticSprite.__init__(self, image, position, layer)

        self.setDistance(0.0)
        self.setSpeed(speed)

    def setDistance(self, distance):
        self.distance = distance

    def setSpeed(self, speed):
        self.speed = speed

    def getDistance(self):
        return self.distance

    def getSpeed(self):
        return self.speed

    def update(self, interval):
        self.distance = interval * self.speed


class CardinalSprite(DynamicSprite):
    def __init__(self, image, position, layer, speed, direction):
        DynamicSprite.__init__(self, image, position, layer, speed) 

        self.setDirection(direction)

    def setDirection(self, direction):
        self.direction = Vector2D(Cardinal().getUnitVectorByDirection(direction))

    def getDirection(self):
        return self.direction

    def update(self, interval):
        DynamicSprite.update(self, interval)

        self.position += self.direction * self.distance

        self.centering()


class HipparchusSprite(DynamicSprite):
    def __init__(self, image, position, layer, speed, angle):
        DynamicSprite.__init__(self, image, position, layer, speed) 

        self.setAngle(angle)

    def setAngle(self, angle):
        self.angle = Hipparchus().getRadiansByDegrees(angle)
        
    def getAngle(self):
        return self.angle

    def update(self, interval):
        DynamicSprite.update(self, interval)

        dx = math.sin(self.angle)
        dy = math.cos(self.angle)

        vector = Vector2D (dx, dy)

        self.position += vector * self.distance

        self.centering()


def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))

    background = load_image("sprite/background.jpg")[0]

    sprites = []

    sprites.append(StaticSprite("sprite/sprite-1.png", (screen.get_rect().center), 10))
    sprites.append(HipparchusSprite("sprite/sprite-2.png", (screen.get_rect().center), 9, 80, 60))
    sprites.append(CardinalSprite("sprite/sprite-3.png", (screen.get_rect().center), 8, 40, 'East'))
    sprites.append(CardinalSprite("sprite/sprite-4.png", (screen.get_rect().center), 7, 40, 'South'))
    sprites.append(CardinalSprite("sprite/sprite-5.png", (screen.get_rect().center), 6, 40, 'West'))
    sprites.append(CardinalSprite("sprite/sprite-6.png", (screen.get_rect().center), 5, 40, 'North'))
    sprites.append(CardinalSprite("sprite/sprite-7.png", (screen.get_rect().center), 4, 40, 'SouthEast'))
    sprites.append(CardinalSprite("sprite/sprite-8.png", (screen.get_rect().center), 3, 40, 'SouthWest'))
    sprites.append(CardinalSprite("sprite/sprite-9.png", (screen.get_rect().center), 2, 40, 'NorthWest'))
    sprites.append(CardinalSprite("sprite/sprite-1.png", (screen.get_rect().center), 1, 40, 'NorthEast'))
    sprites.append(CardinalSprite("sprite/sprite-2.png", (screen.get_rect().center), 0, 80, 'Random'))

    group = pygame.sprite.LayeredUpdates((sprites))

    screen.blit(background, (0, 0))
    pygame.display.update()

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        time_passed_seconds = clock.tick() / 1000.0

        group.update(time_passed_seconds)
        group.clear(screen, background)
        changes = group.draw(screen)
        pygame.display.update(changes)


if __name__ == '__main__': main()

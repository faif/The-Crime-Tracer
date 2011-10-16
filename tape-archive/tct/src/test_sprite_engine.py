try:
    import random
    import pygame
    import graphics

    from resource_manager import ResourceManager

    from sprite_engine import *
except (RuntimeError, ImportError) as error:
    import os, constants
    path = os.path.basename(__file__)
    print('{0}: {1}'.format(path, error))
    exit(constants.MOD_FAIL_ERR)


class StaticGO(StaticSprite):
    def __init__(self, file, position, layer, alpha, reuse):
        super(StaticGO, self).__init__(file, position, layer, alpha, reuse)


class CardinalGO(CardinalSprite):
    def __init__(self, file, position, layer, alpha, reuse, speed, area, direction):
        super(CardinalGO, self).__init__(file, position, layer, alpha, reuse, speed, area, direction)

    def update(self, interval):
        super(CardinalGO, self).update(interval)

        self.arrangeRectangle()

        if not self._limiter is None:
            self._limiter.run(self)


class ShakingGO(ShakingSprite):
    def __init__(self, file, position, layer, alpha, reuse, speed, area):
        super(ShakingGO, self).__init__(file, position, layer, alpha, reuse, speed, area)

    def update(self, interval):
        super(ShakingGO, self).update(interval)

        self.arrangeRectangle()

        if not self._limiter is None:
            self._limiter.run(self)


class HipparchusGO(HipparchusSprite):
    def __init__(self, file, position, layer, alpha, reuse, speed, area, angle):
        super(HipparchusGO, self).__init__(file, position, layer, alpha, reuse, speed, area, angle)

    def update(self, interval):
        super(HipparchusGO, self).update(interval)

        self.arrangeRectangle()

        if not self._limiter is None:
            self._limiter.run(self)


class TravelGO(TravelSprite):
    def __init__(self, file, position, layer, alpha, reuse, speed, area):
        super(TravelGO, self).__init__(file, position, layer, alpha, reuse, speed, area)

    def update(self, interval):
        super(TravelGO, self).update(interval)

        if self.travels():
            if self.arrived():
                self.stop()
            else:
                self.approach()

        self.arrangeRectangle()

        if not self._limiter is None:
            self._limiter.run(self)


class ExplosionGO(StaticAnimation):
    def __init__(self, sheet, position, layer, alpha, reuse, width, height, fps):
        super(ExplosionGO, self).__init__(sheet, position, layer, alpha, reuse, width, height, fps)

    def update(self, interval):
        super(ExplosionGO, self).update(interval)

        self.arrangeRectangle()


class RunningGO(StaticAnimation):
    def __init__(self, sheet, position, layer, alpha, reuse, width, height, fps):
        super(RunningGO, self).__init__(sheet, position, layer, alpha, reuse, width, height, fps)

    def update(self, interval):
        super(RunningGO, self).update(interval)

        self.arrangeRectangle()


def main():
    pygame.init()

    SCREEN_SIZE = (800, 600)

    screen = pygame.display.set_mode(SCREEN_SIZE)

    area = screen.get_rect()

    half = area.inflate((-SCREEN_SIZE[0]/2., -SCREEN_SIZE[1]/2.))

    resourceManager = ResourceManager()

    resourceManager.setResourcesPath("resources")
    resourceManager.setImagesPath("graphics")

    defaultLimiter = LimiterFactory().getInstance('Default')

    sprites = []

    sprites.append(ShakingGO("sprite/sprite-1.png", (area.center), random.randint(0, 30), random.randint(20, 255), False, random.randint(50, 150), area))
    sprites.append(ShakingGO("sprite/sprite-2.png", (area.center), random.randint(0, 30), random.randint(20, 255), False, random.randint(50, 150), area))

    sprites.append(CardinalGO("sprite/sprite-3.png", (area.center), random.randint(0, 30), random.randint(20, 255), False, random.randint(50, 150), area, 'West'))
    sprites.append(CardinalGO("sprite/sprite-4.png", (area.center), random.randint(0, 30), random.randint(20, 255), False, random.randint(50, 150), area, 'North'))

    sprites.append(HipparchusGO("sprite/sprite-5.png", (area.center), random.randint(0, 30), random.randint(20, 255), False, random.randint(50, 150), area, 'Random'))
    sprites.append(HipparchusGO("sprite/sprite-6.png", (area.center), random.randint(0, 30), random.randint(20, 255), False, random.randint(50, 150), area, 'Random'))

    sprites.append(StaticGO("sprite/sprite-7.png", (area.center), random.randint(0, 30), random.randint(20, 255), False))

    hipparchusGO = HipparchusGO("sprite/sprite-9.png", (half.center), random.randint(0, 30), random.randint(20, 255), False, random.randint(50, 150), half, 'Random')
    shakingGO = ShakingGO("sprite/sprite-9.png", (half.center), random.randint(0, 30), random.randint(20, 255), True, random.randint(50, 150), half)
    travelGO = TravelGO("sprite/sprite-1.png", (half.center), random.randint(0, 30), random.randint(20, 255), False, random.randint(50, 150), half)

    sprites.append(hipparchusGO)
    sprites.append(shakingGO)
    sprites.append(travelGO)

    for sprite in sprites:
        sprite.limiter = defaultLimiter

    explosionGO = ExplosionGO("sprite/explosion.png", (area.center), random.randint(0, 30), random.randint(20, 255), False, 20, 20, 10)
    runningGO = RunningGO("sprite/character-hand.png", (area.center), random.randint(0, 30), random.randint(20, 255), False, 50, 72, 10)

    sprites.append(explosionGO)
    sprites.append(runningGO)

    group = pygame.sprite.LayeredUpdates((sprites))

    background = ResourceManager().getImage("sprite/background.jpg")

    screen.blit(background, (0, 0))

    pygame.display.update()

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEMOTION:
                travelGO.destination = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                shakingGO.position = pygame.mouse.get_pos()
                shakingGO._layer = random.choice(group.layers())
                shakingGO.speed = random.randint(50, 150)
                shakingGO.alpha = random.randint(20, 255)
                travelGO.move()
            elif event.type == pygame.MOUSEBUTTONUP:
                travelGO.still()
            elif event.type == pygame.KEYDOWN:
                hipparchusGO.position = pygame.mouse.get_pos()
                hipparchusGO._layer = random.choice(group.layers())
                hipparchusGO.speed = random.randint(50, 150)

                runningGO.position = pygame.mouse.get_pos()
                explosionGO._layer = random.choice(group.layers())
                explosionGO.alpha = random.randint(20, 255)

        time_passed_seconds = clock.tick() / 1000.0

        print clock.get_fps()

        group.update(time_passed_seconds)
        group.clear(screen, background)
        changes = group.draw(screen)
        pygame.display.update(changes)


if __name__ == '__main__': main()

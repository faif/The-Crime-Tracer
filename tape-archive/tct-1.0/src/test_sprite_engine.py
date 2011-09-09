try:
    import random
    import pygame
    import graphics

    from sprite_engine import *
except (RuntimeError, ImportError) as error:
    import os, constants
    path = os.path.basename(__file__)
    print('{0}: {1}'.format(path, error))
    exit(constants.MOD_FAIL_ERR)


def main():
    pygame.init()

    SCREEN_SIZE = [800, 600]

    screen = pygame.display.set_mode(SCREEN_SIZE)

    area = screen.get_rect()

    area.inflate_ip((-SCREEN_SIZE[0]/2,
                     -SCREEN_SIZE[1]/2))

    sprites = []

    factory = SpriteFactory()

    sprites.append(factory.getSprite("Insistence", "sprite/sprite-1.png", (area.center), random.randint(0, 30), random.randint(20, 255), random.randint(50, 150), area, 'Random'))
    sprites.append(factory.getSprite("Insistence", "sprite/sprite-2.png", (area.center), random.randint(0, 30), random.randint(20, 255), random.randint(50, 150), area, 'Random'))

    sprites.append(factory.getSprite("Cardinal", "sprite/sprite-3.png", (area.center), random.randint(0, 30), random.randint(20, 255), random.randint(50, 150), area, 'West'))
    sprites.append(factory.getSprite("Cardinal", "sprite/sprite-4.png", (area.center), random.randint(0, 30), random.randint(20, 255), random.randint(50, 150), area, 'North'))

    sprites.append(factory.getSprite("Hipparchus", "sprite/sprite-5.png", (area.center), random.randint(0, 30), random.randint(20, 255), random.randint(50, 150), area, random.randint(0, 360)))
    sprites.append(factory.getSprite("Hipparchus", "sprite/sprite-6.png", (area.center), random.randint(0, 30), random.randint(20, 255), random.randint(50, 150), area, random.randint(0, 360)))

    sprites.append(StaticSprite("sprite/sprite-7.png", (area.center), random.randint(0, 30), random.randint(20, 255)))

    changable1 = factory.getSprite("Hipparchus", "sprite/sprite-8.png", (area.center), random.randint(0, 30), random.randint(20, 255), random.randint(50, 150), area, 'Random')
    changable2 = factory.getSprite("Insistence", "sprite/sprite-9.png", (area.center), random.randint(0, 30), random.randint(20, 255), random.randint(50, 150), area, 'Random')

    sprites.append(changable1)
    sprites.append(changable2)

    group = pygame.sprite.LayeredUpdates((sprites))

    background = graphics.load_image("sprite/background.jpg")[0]

    screen.blit(background, (0, 0))

    pygame.display.update()

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                changable1.position = pygame.mouse.get_pos()
                changable1._layer = random.choice(group.layers())
                changable1.speed = random.randint(50, 150)
                changable1.alpha = random.randint(255, 255)
            elif event.type == pygame.KEYDOWN:
                changable2.position = pygame.mouse.get_pos()
                changable2._layer = random.choice(group.layers())
                changable2.speed = random.randint(50, 150)
                changable2.alpha = random.randint(255, 255)

        time_passed_seconds = clock.tick() / 1000.0

        print clock.get_fps()

        group.update(time_passed_seconds)
        group.clear(screen, background)
        changes = group.draw(screen)
        pygame.display.update(changes)


if __name__ == '__main__': main()

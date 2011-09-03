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

    screen = pygame.display.set_mode((800, 600))

    background = graphics.load_image("sprite/background.jpg")[0]

    sprites = []

    sprites.append(StaticSprite("sprite/sprite-9.png", (screen.get_rect().center), 0))

    sprites.append(SpriteFactory().getSprite("Insistence", "sprite/sprite-8.png", (screen.get_rect().center), 1, 200, 'Random'))

    sprites.append(SpriteFactory().getSprite("Cardinal", "sprite/sprite-1.png", (screen.get_rect().center), 2, 20, 'East'))
    sprites.append(SpriteFactory().getSprite("Cardinal", "sprite/sprite-2.png", (screen.get_rect().center), 3, 20, 'South'))
    sprites.append(SpriteFactory().getSprite("Cardinal", "sprite/sprite-3.png", (screen.get_rect().center), 4, 20, 'West'))
    sprites.append(SpriteFactory().getSprite("Cardinal", "sprite/sprite-4.png", (screen.get_rect().center), 5, 20, 'North'))
    sprites.append(SpriteFactory().getSprite("Cardinal", "sprite/sprite-5.png", (screen.get_rect().center), 6, 20, 'SouthEast'))
    sprites.append(SpriteFactory().getSprite("Cardinal", "sprite/sprite-6.png", (screen.get_rect().center), 7, 20, 'SouthWest'))
    sprites.append(SpriteFactory().getSprite("Cardinal", "sprite/sprite-7.png", (screen.get_rect().center), 8, 20, 'NorthWest'))
    sprites.append(SpriteFactory().getSprite("Cardinal", "sprite/sprite-8.png", (screen.get_rect().center), 9, 20, 'NorthEast'))
    sprites.append(SpriteFactory().getSprite("Cardinal", "sprite/sprite-9.png", (screen.get_rect().center), 10, 40, 'Random'))

    sprites.append(SpriteFactory().getSprite("Hipparchus", "sprite/sprite-1.png", (screen.get_rect().center), 11, random.randint(10, 100), random.randint(0, 360)))
    sprites.append(SpriteFactory().getSprite("Hipparchus", "sprite/sprite-2.png", (screen.get_rect().center), 12, random.randint(10, 100), random.randint(0, 360)))
    sprites.append(SpriteFactory().getSprite("Hipparchus", "sprite/sprite-3.png", (screen.get_rect().center), 13, random.randint(10, 100), random.randint(0, 360)))
    sprites.append(SpriteFactory().getSprite("Hipparchus", "sprite/sprite-4.png", (screen.get_rect().center), 14, random.randint(10, 100), random.randint(0, 360)))
    sprites.append(SpriteFactory().getSprite("Hipparchus", "sprite/sprite-5.png", (screen.get_rect().center), 15, random.randint(10, 100), random.randint(0, 360)))
    sprites.append(SpriteFactory().getSprite("Hipparchus", "sprite/sprite-6.png", (screen.get_rect().center), 16, random.randint(10, 100), random.randint(0, 360)))
    sprites.append(SpriteFactory().getSprite("Hipparchus", "sprite/sprite-7.png", (screen.get_rect().center), 17, random.randint(10, 100), random.randint(0, 360)))
    sprites.append(SpriteFactory().getSprite("Hipparchus", "sprite/sprite-8.png", (screen.get_rect().center), 18, random.randint(10, 100), random.randint(0, 360)))
    sprites.append(SpriteFactory().getSprite("Hipparchus", "sprite/sprite-9.png", (screen.get_rect().center), 19, random.randint(10, 100), random.randint(0, 360)))

    changable1 = SpriteFactory().getSprite("Hipparchus", "sprite/sprite-1.png", (screen.get_rect().center), 20, 40, 'Random')
    changable2 = SpriteFactory().getSprite("Hipparchus", "sprite/sprite-1.png", (screen.get_rect().center), 21, 40, 'Random')

    sprites.append(changable1)
    sprites.append(changable2)

    group = pygame.sprite.LayeredUpdates((sprites))

    screen.blit(background, (0, 0))

    pygame.display.update()

    clock = pygame.time.Clock()

    pygame.key.set_repeat(1, 200)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                changable1.setPosition(event.pos)
                changable1.setImage("sprite/sprite-" + str(random.randint(1, 9)) + ".png")
                changable1.setLayer(random.choice(group.layers()))
                changable1.setAngle(random.randint(0, 360))
                changable1.setSpeed(random.randint(10, 200))
            elif event.type == pygame.KEYDOWN:
                changable2.setPosition(pygame.mouse.get_pos())
                changable2.setImage("sprite/sprite-" + str(random.randint(1, 9)) + ".png")
                changable2.setLayer(random.choice(group.layers()))
                changable1.setAngle(random.randint(0, 360))
                changable2.setSpeed(random.randint(10, 200))

        time_passed_seconds = clock.tick() / 1000.0

        group.update(time_passed_seconds)
        group.clear(screen, background)
        changes = group.draw(screen)
        pygame.display.update(changes)


if __name__ == '__main__': main()

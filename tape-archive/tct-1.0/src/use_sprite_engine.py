try:
    import random
    import pygame
    import graphics

    import sprite_engine
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

    sprites.append(sprite_engine.SpriteFactory().getSprite("Insistence", "sprite/sprite-1.png", (screen.get_rect().center), random.randint(0, 30), random.randint(20, 255), random.randint(50, 150), 'Random'))

    sprites.append(sprite_engine.SpriteFactory().getSprite("Cardinal", "sprite/sprite-2.png", (screen.get_rect().center), random.randint(0, 30), random.randint(20, 255), random.randint(50, 150), 'East'))
    sprites.append(sprite_engine.SpriteFactory().getSprite("Cardinal", "sprite/sprite-3.png", (screen.get_rect().center), random.randint(0, 30), random.randint(20, 255), random.randint(50, 150), 'South'))
    sprites.append(sprite_engine.SpriteFactory().getSprite("Cardinal", "sprite/sprite-4.png", (screen.get_rect().center), random.randint(0, 30), random.randint(20, 255), random.randint(50, 150), 'West'))
    sprites.append(sprite_engine.SpriteFactory().getSprite("Cardinal", "sprite/sprite-5.png", (screen.get_rect().center), random.randint(0, 30), random.randint(20, 255), random.randint(50, 150), 'North'))
    sprites.append(sprite_engine.SpriteFactory().getSprite("Cardinal", "sprite/sprite-6.png", (screen.get_rect().center), random.randint(0, 30), random.randint(20, 255), random.randint(50, 150), 'SouthEast'))
    sprites.append(sprite_engine.SpriteFactory().getSprite("Cardinal", "sprite/sprite-7.png", (screen.get_rect().center), random.randint(0, 30), random.randint(20, 255), random.randint(50, 150), 'SouthWest'))
    sprites.append(sprite_engine.SpriteFactory().getSprite("Cardinal", "sprite/sprite-8.png", (screen.get_rect().center), random.randint(0, 30), random.randint(20, 255), random.randint(50, 150), 'NorthWest'))
    sprites.append(sprite_engine.SpriteFactory().getSprite("Cardinal", "sprite/sprite-9.png", (screen.get_rect().center), random.randint(0, 30), random.randint(20, 255), random.randint(50, 150), 'NorthEast'))
    sprites.append(sprite_engine.SpriteFactory().getSprite("Cardinal", "sprite/sprite-1.png", (screen.get_rect().center), random.randint(0, 30), random.randint(20, 255), random.randint(50, 150), 'Random'))

    sprites.append(sprite_engine.SpriteFactory().getSprite("Hipparchus", "sprite/sprite-2.png", (screen.get_rect().center), random.randint(0, 30), random.randint(20, 255), random.randint(50, 150), random.randint(0, 360)))
    sprites.append(sprite_engine.SpriteFactory().getSprite("Hipparchus", "sprite/sprite-3.png", (screen.get_rect().center), random.randint(0, 30), random.randint(20, 255), random.randint(50, 150), random.randint(0, 360)))
    sprites.append(sprite_engine.SpriteFactory().getSprite("Hipparchus", "sprite/sprite-4.png", (screen.get_rect().center), random.randint(0, 30), random.randint(20, 255), random.randint(50, 150), random.randint(0, 360)))
    sprites.append(sprite_engine.SpriteFactory().getSprite("Hipparchus", "sprite/sprite-5.png", (screen.get_rect().center), random.randint(0, 30), random.randint(20, 255), random.randint(50, 150), random.randint(0, 360)))
    sprites.append(sprite_engine.SpriteFactory().getSprite("Hipparchus", "sprite/sprite-6.png", (screen.get_rect().center), random.randint(0, 30), random.randint(20, 255), random.randint(50, 150), random.randint(0, 360)))
    sprites.append(sprite_engine.SpriteFactory().getSprite("Hipparchus", "sprite/sprite-7.png", (screen.get_rect().center), random.randint(0, 30), random.randint(20, 255), random.randint(50, 150), random.randint(0, 360)))
    sprites.append(sprite_engine.SpriteFactory().getSprite("Hipparchus", "sprite/sprite-8.png", (screen.get_rect().center), random.randint(0, 30), random.randint(20, 255), random.randint(50, 150), random.randint(0, 360)))
    sprites.append(sprite_engine.SpriteFactory().getSprite("Hipparchus", "sprite/sprite-9.png", (screen.get_rect().center), random.randint(0, 30), random.randint(20, 255), random.randint(50, 150), random.randint(0, 360)))
    sprites.append(sprite_engine.SpriteFactory().getSprite("Hipparchus", "sprite/sprite-1.png", (screen.get_rect().center), random.randint(0, 30), random.randint(20, 255), random.randint(50, 150), random.randint(0, 360)))

    sprites.append(sprite_engine.StaticSprite("sprite/sprite-5.png", (screen.get_rect().center), random.randint(0, 30), random.randint(20, 255)))

    changable1 = sprite_engine.SpriteFactory().getSprite("Hipparchus", "sprite/sprite-6.png", (screen.get_rect().center), random.randint(0, 30), random.randint(20, 255), random.randint(50, 150), 'Random')
    changable2 = sprite_engine.SpriteFactory().getSprite("Insistence", "sprite/sprite-7.png", (screen.get_rect().center), random.randint(0, 30), random.randint(20, 255), random.randint(50, 150), 'Random')

    sprites.append(changable1)
    sprites.append(changable2)

    group = pygame.sprite.LayeredUpdates((sprites))

    screen.blit(background, (0, 0))

    pygame.display.update()

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                changable1.setPosition(pygame.mouse.get_pos())
                changable1.setLayer(random.choice(group.layers()))
                changable1.setAngle(random.randint(0, 360))
                changable1.setSpeed(random.randint(50, 150))
                changable1.setAlpha(random.randint(20, 255))
            elif event.type == pygame.KEYDOWN:
                changable2.setPosition(pygame.mouse.get_pos())
                changable2.setLayer(random.choice(group.layers()))
                changable2.setSpeed(random.randint(50, 150))
                changable2.setAlpha(random.randint(20, 255))

        time_passed_seconds = clock.tick() / 1000.0

        group.update(time_passed_seconds)
        group.clear(screen, background)
        changes = group.draw(screen)
        pygame.display.update(changes)


if __name__ == '__main__': main()

try:
    import unittest
    import pygame
    import anim_sprite
    import constants
    from anim_sprite import *
except ImportError as err:
    try:
        import os
        path = os.path.basename(__file__)
        print((': '.join((path, str(err)))))
    except ImportError:
        print((': '.join(("couldn't load module", str(err)))))
    exit(2)

# code required to make the script work
pygame.init()
pygame.display.set_mode(
    (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), 0)
sprite_fact = SpriteFactory()

class BadInput(unittest.TestCase):
    '''Tests related with bad input given in anim_sprite.'''

    def test_min_speed(self):
        '''create_anim_sprite should fail with speed values < min. acceptable'''
        self.assertRaises(ValueError, 
                          sprite_fact.create_anim_sprite, 
                          anim_sprite.VERT_ANIM,
                          constants.FILES['graphics']['menu']['share']['anim'][0],
                          anim_sprite.MIN_SPEED - 1)

    def test_max_speed(self):
        '''create_anim_sprite should fail with speed values > max. acceptable'''
        self.assertRaises(ValueError, 
                          sprite_fact.create_anim_sprite, 
                          anim_sprite.VERT_ANIM,
                          constants.FILES['graphics']['menu']['share']['anim'][0],
                          anim_sprite.MAX_SPEED + 1)

if __name__ == '__main__':
    unittest.main()

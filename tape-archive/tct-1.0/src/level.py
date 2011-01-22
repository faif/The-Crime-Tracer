try:
    import constants
    from base import Base
    from fsm import State
    from os_utils import safe_exit
except ImportError as err:
    try:
        import os
        path = os.path.basename(__file__)
        print((': '.join((path, str(err)))))
    # importing os failed, print a custom message...
    except ImportError:
        print((': '.join(("couldn't load module", str(err)))))
    exit(2)

## objects imported when `from <module> import *' is used
__all__ = ['LevelFactory']

## the "right" way to create a new level (exposed interface)
#
class LevelFactory(Base):

    ## create a new level
    #
    # @param self the object pointer
    # @param name the level's name
    def create_level(self, name, game_opts):
        # find out which factory to use
        if (name == constants.SCENES['level_one']):
            self.factory = LevelOne(game_opts)
        else:
            raise ValueError('No such level', name)

        # build the actual level
        assert(self.factory is not None)
        lev =  self.factory.create_level()
        assert(lev is not None)
        # return the object instance to the game manager
        return self.factory


## one factory for each level because there might be
## differences (different number and type of rooms, etc)
#
class LevelOne(State):
    def __init__(self, game_opts):
        # initialize the state
        State.__init__(self, constants.SCENES['level_one'])
        self.game_opts = game_opts

    # rooms, doors, obstacles, etc.
    def create_level(self):
        print('creating level 1')
        r1 = self.create_room('office')
        r2 = self.create_room('park')
        lev = (r1, r2)
        return lev
        
    def create_room(self, name):
        return Room(name)

    def create_door(self, colour):
        return Door(colour)

    ## what to do when the level is enabled
    #
    # @param self the object pointer
    def do_actions(self):
        print('exiting...')
        safe_exit()

## not necessary but makes inheritance more clear
#
class MapSite: pass

class Room(MapSite):
    def __init__(self, name):
        self.name = name

    def enter(self):
        print('entering a room')

class Door(MapSite):
    def __init__(self, colour):
        self.colour = colour

    def enter(self):
        print('entering a door')

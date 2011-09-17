try:
    import pygame

    from os import path
    from pygame.locals import *

    from borg import Borg
except (RuntimeError, ImportError) as error:
        import os, constants
        path = os.path.basename(__file__)
        print('{0}: {1}'.format(path, error))
        exit(constants.MOD_FAIL_ERR)


class ResourceManager(Borg):
    __images = {}

    __resources_path = None

    __images_path = None

    def setResourcesPath(self, path):
        ResourceManager.__resources_path = path

    def getImage(self, file, colorKey = -1, reuse = False):
        if not ResourceManager.__resources_path:
            raise ValueError ("ResourceManager.setResourcesPath() not called yet.")

        if not ResourceManager.__images_path:
            raise ValueError ("ResourceManager.setImagesPath() not called yet.")

        if (reuse and file in ResourceManager.__images.keys()):
            return ResourceManager.__images[file]
        else:
            try:
                fullpath = path.join(ResourceManager.__resources_path, ResourceManager.__images_path, file)

                image = pygame.image.load(fullpath)
            except pygame.error as error:
                raise IOError ("Couldn't load image: {0}".format(fullpath))

            if image.get_alpha() is None:
                image = image.convert()
            else:
                image = image.convert_alpha()

            if colorKey:
                if colorKey is -1:
                    colorKey = image.get_at((0, 0))

                image.set_colorkey(colorKey, RLEACCEL)

            ResourceManager.__images[file] = image

            return image

    def setImagesPath(self, path):
        ResourceManager.__images_path = path

    def hasImage(self, file):
        return ResourceManager.__images.has_key(file)

    def clearImage(self, file):
        try:
            del ResourceManager.__images[file]
            return True
        except KeyError:
            return False

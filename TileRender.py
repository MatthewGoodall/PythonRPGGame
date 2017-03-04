import pytmx
<<<<<<< HEAD
from pytmx.util_pygame import load_pygame

from CollisionObject import *
=======
from CollisionObject import*
>>>>>>> origin/master
from Player import *


class Renderer(object):
    """
    This object renders tile maps from Tiled
    """

    def __init__(self, filename):
<<<<<<< HEAD
        tm = load_pygame(filename, pixelAlpha=True)
=======
        tm = pytmx.util_pygame.load_pygame(filename, pixel_alpha=True)
>>>>>>> origin/master
        self.size = tm.width * tm.tilewidth, tm.height * tm.tileheight
        self.tmx_data = tm
        self.walls = list()

    def render(self, surface):

        tw = self.tmx_data.tilewidth
        th = self.tmx_data.tileheight
        gt = self.tmx_data.get_tile_image_by_gid

        if self.tmx_data.background_color:
            surface.fill(pygame.Color(self.tmx_data.background_color))

        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = gt(gid)
                    if tile:
                        surface.blit(tile, (x * tw, y * th))

            if isinstance(layer, pytmx.TiledObjectGroup):
                if layer.name == "objects":
                    print("yes")
                    for obj in layer:
                        collision_object = CollisionObject(obj.x, obj.y, obj.width, obj.height)
                        self.walls.append(collision_object)

            elif isinstance(layer, pytmx.TiledImageLayer):
                image = gt(layer.gid)
                if image:
                    surface.blit(image, (0, 0))

    def make_map(self):
        temp_surface = pygame.Surface(self.size)
        self.render(temp_surface)
        return temp_surface

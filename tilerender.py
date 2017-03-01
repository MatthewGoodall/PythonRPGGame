import pygame 

import pytmx
from pytmx.util_pygame import load_pygame

class Renderer(object):
    """
    This object renders tile maps from Tiled
    """

    def __init__(self, filename):
        tm = load_pygame(filename, pixelalpha=True)
        self.size = tm.width * tm.tilewidth, tm.height * tm.tileheight
        self.tmx_data = tm

    def render(self, surface):

        tw = self.tmx_data.tilewidth
        th = self.tmx_data.tileheight
        gt = self.tmx_data.get_tile_image_by_gid

        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = gt(gid)
                    if tile:
                        surface.blit(tile, (x * tw, y * th))

            elif isinstance(layer, pytmx.TiledObjectGroup):
                pass

            elif isinstance(layer, pytmx.TiledImageLayer):
                image = gt(layer.gid)
                if image:
                    surface.blit(image, (0, 0))

    def make_map(self):
        temp_surface = pygame.Surface(self.size)
        self.render(temp_surface)
        return temp_surface

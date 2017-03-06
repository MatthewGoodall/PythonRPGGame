import pytmx
from pytmx.util_pygame import load_pygame
import CollisionObject
from Player import *


class Renderer(object):
    """
    This object renders tile maps from Tiled
    """

    def __init__(self, filename):
        tm = pytmx.util_pygame.load_pygame(filename, pixel_alpha=True)
        self.size = tm.width * tm.tilewidth, tm.height * tm.tileheight
        self.tmx_data = tm
        self.ground = []
        self.platforms = []
        self.ladders = []

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
                if layer.name == "Collisions":
                    for obj in layer:
                        if obj.type == "Platform":
                            a_platform = CollisionObject.Platform(obj.x, obj.y, obj.width, obj.height)
                            self.platforms.append(a_platform)
                        elif obj.type == "Ladder":
                            a_ladder = CollisionObject.Ladder(obj.x, obj.y, obj.width, obj.height)
                            self.ladders.append(a_ladder)
                        elif obj.type == "Solid":
                            ground_piece = CollisionObject.CollisionObject(obj.x, obj.y, obj.width, obj.height)
                            self.ground.append(ground_piece)

            elif isinstance(layer, pytmx.TiledImageLayer):
                image = gt(layer.gid)
                if image:
                    surface.blit(image, (0, 0))

    def make_map(self):
        temp_surface = pygame.Surface(self.size)
        self.render(temp_surface)
        return temp_surface

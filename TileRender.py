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
        self.objects = list()

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
                        if obj.name == "Platform":
                            collision_object = CollisionObject.Platform(obj.x, obj.y, obj.width, obj.height)
                        elif obj.name == "Ladder":
                            collision_object = CollisionObject.Ladder(obj.x, obj.y, obj.width, obj.height)
                            print("a ladder")
                        else:
                            collision_object = CollisionObject.CollisionObject(obj.x, obj.y, obj.width, obj.height)
                        self.objects.append(collision_object)

            elif isinstance(layer, pytmx.TiledImageLayer):
                image = gt(layer.gid)
                if image:
                    surface.blit(image, (0, 0))

    def make_map(self):
        temp_surface = pygame.Surface(self.size)
        self.render(temp_surface)
        return temp_surface

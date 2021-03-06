import pytmx
from pytmx.util_pygame import load_pygame
import pygame
import CollisionObject


class Renderer(object):
    """
    This object renders tile maps from Tiled
    """
    all_gateways = []
    def __init__(self, filename):
        tm = pytmx.util_pygame.load_pygame(filename, pixel_alpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.size = self.width, self.height
        self.tmx_data = tm
        self.solids = []
        self.platforms = []
        self.ladders = []
        self.gateways = []

    def Render(self, surface):

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
                            solid_piece = CollisionObject.SolidObject(obj.x, obj.y, obj.width, obj.height)
                            self.solids.append(solid_piece)
                        elif obj.type == "Gateway":
                            a_gateway = CollisionObject.Gateway(obj.x, obj.y, obj.width, obj.height,
                                                                obj.name, obj.properties["travel_location"],
                                                               )
                            self.gateways.append(a_gateway)
                            self.all_gateways.append(a_gateway)

            elif isinstance(layer, pytmx.TiledImageLayer):
                image = gt(layer.gid)
                if image:
                    surface.blit(image, (0, 0))

    def MakeMap(self):
        temp_surface = pygame.Surface(self.size)
        self.Render(temp_surface)
        return temp_surface

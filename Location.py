import TileRender
import Camera
import NPC
import Enemy


class Location():
    def __init__(self, level_tmx_map_path):
        self.enemies = []
        self.NPCs = []
        self.tmx_map_path = level_tmx_map_path
        self.tile_renderer = None
        self.map_surface = None
        self.map_rect = None

        self.collisions = None
        self.platforms = None
        self.solids = None
        self.ladders = None

        self.width = None
        self.height = None

    def CreateMap(self):
        self.tile_renderer = TileRender.Renderer(self.tmx_map_path)
        self.map_surface = self.tile_renderer.MakeMap()
        self.map_rect = self.map_surface.get_rect()
        self.platforms = self.tile_renderer.platforms
        self.solids = self.tile_renderer.solids
        self.ladders = self.tile_renderer.ladders
        self.collisions = self.platforms + self.solids + self.ladders

        self.width = self.tile_renderer.width
        self.height = self.tile_renderer.height

    def Render(self, screen):
        self.tile_renderer.Render(screen)

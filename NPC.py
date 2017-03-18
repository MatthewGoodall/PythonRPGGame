import pygame


class NPC(pygame.sprite.Sprite):
    def __init__(self, npc_data, index):
        super().__init__()
        self.name = npc_data[index]["name"]
        self.location = npc_data[index]["location"]
        self.image = pygame.image.load(npc_data[index]["image path"]).convert_alpha()
        self.close_up = pygame.image.load(npc_data[index]["closeup path"]).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = int( npc_data[index]["x pos"] )
        self.rect.y = int( npc_data[index]["y pos"] )
        self.dialogue = npc_data[index]["dialogue"]

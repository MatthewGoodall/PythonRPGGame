import pygame


class NPC(pygame.sprite.Sprite):
    def __init__(self, name, location, image_path, x, y, dialogue):
        super().__init__()
        self.name = name
        self.location = location
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dialogue = dialogue

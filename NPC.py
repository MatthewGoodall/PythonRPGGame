import pygame


class NPC(pygame.sprite.Sprite):
    image = pygame.image.load("Resources\SinglePhotos\DragonEgg.png")

    def __init__(self, x, y):
        super().__init__()

        self.image = NPC.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

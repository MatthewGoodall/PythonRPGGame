import pygame
import Animation


class GUI_Item(pygame.sprite.Sprite):
    def __init__(self, spritesheet, x, y):
        super().__init__()
        self.image = spritesheet.get_first_frame()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

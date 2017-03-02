import pygame
import Animation


class GUI_Item(pygame.sprite.Sprite):
    def __init__(self, spritesheet, x, y):
        super().__init__()
        self.image = spritesheet.get_first_frame()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


health_bar = GUI_Item(Animation.health_bar_anim, 0, 0)
mana_bar = GUI_Item(Animation.mana_bar_anim, 65 * 2, 0)

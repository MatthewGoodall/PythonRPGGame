import pygame
import TextWrapper
import copy

class MessageBox(pygame.sprite.Sprite):
    def __init__(self, frame_image, font, npc):
        super().__init__()

        self.image = copy.copy(frame_image)
        self.dialogue_box = pygame.Surface((800, 200), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 385
        self.dialogue_box_rect = self.dialogue_box.get_rect()
        TextWrapper.drawText(self.dialogue_box, npc.dialogue, (0, 0, 0), self.dialogue_box_rect, font)
        self.image.blit(self.dialogue_box, (204, 16))
        self.image.blit(npc.close_up, (12, 12))

    def Update(self, game):
        pass

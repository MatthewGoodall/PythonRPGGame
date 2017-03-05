import pygame
import Animation

class NPC(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.NPC_name = name
        self.health = 100

        self.idle_animation = Animation.npc_idle

        self.image = self.current_animation.get_first_frame()

        self.rect = self.image.get_rect()

    def UpdateAnimation(self, time):
        if self.current_animation.needsUpdate(time):
            self.image = self.current_animation.update()

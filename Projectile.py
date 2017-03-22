import pygame
class Projectile(pygame.sprite.Sprite):
    def __init__(self, attack, x, y):
        self.image = attack.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = attack.speed

    def Update(self):
        self.rect.x += self.speed

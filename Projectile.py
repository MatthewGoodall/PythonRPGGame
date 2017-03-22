import pygame
class Projectile(pygame.sprite.Sprite):
    def __init__(self, attack, x, y):
        self.attack = attack
        self.image = attack.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = attack.speed

    def Update(self, game):
        self.rect.x += self.speed
        collisions = pygame.sprite.spritecollide(self, game.current_location.enemies, False)
        for hit in collisions:
            hit.TakeDamage(self.attack.damage)
            game.projectiles.remove(self)

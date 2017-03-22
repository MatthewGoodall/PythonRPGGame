import pygame
class Projectile(pygame.sprite.Sprite):
    def __init__(self, attack, x, y):
        self.attack = attack
        self.image = attack.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = attack.speed
        self.direction = 1

    def Update(self, game):
        self.rect.x += self.speed * self.direction
        collisions = pygame.sprite.spritecollide(self, game.current_enemies, False)
        for hit in collisions:
            hit.TakeDamage(self.attack.damage)
            game.projectiles.remove(self)

    def UpdateDirection(self, new_direction):
        if new_direction == "right":
            self.direction = 1
        elif new_direction == "left":
            self.direction = -1

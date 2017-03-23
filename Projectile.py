import pygame
import copy

class Projectile(pygame.sprite.Sprite):
    def __init__(self, attack, x, y):
        self.attack = attack
        self.right_animation = copy.copy(attack.animation)
        self.left_animation = self.right_animation.GetMirrorAnimation()
        self.current_animation = self.right_animation
        self.image = self.current_animation.GetFirstFrame()
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
            self.ChangeCurrentAnimation("right")
            self.image = self.current_animation.GetFirstFrame()
        elif new_direction == "left":
            self.direction = -1
            self.ChangeCurrentAnimation("left")
            self.image = self.current_animation.GetFirstFrame()

    def UpdateAnimation(self, time):
        if self.current_animation.NeedsUpdate(time):
            self.image = self.current_animation.Update()

    def ChangeCurrentAnimation(self, direction):
        if direction == "right":
            self.current_animation = self.right_animation
        elif direction == "left":
            self.current_animation = self.left_animation

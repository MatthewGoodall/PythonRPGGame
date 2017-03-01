import pygame
import Animation
from Enemy import *

pygame.mixer.init()
pygame.display.init()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.current_health = 10
        self.speed = 5.0
        self.random_value = 2.0
        self.idle_right_animation = Animation.player_idle_right
        self.idle_left_animation = Animation.player_idle_left
        self.walking_right_animation = Animation.player_walking_right
        self.walking_left_animation = Animation.player_walking_left
        self.current_animation = self.idle_right_animation

        self.image = self.current_animation.get_first_frame()

        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 500

        self.moving_right = False
        self.moving_left = False
        self.touching_ground = True
        self.jumping = False
        self.can_jump = True
        self.y_speed = 0.0
        self.last_direction = "right"

        self.world_shift = 0
        self.level_limit = -1000
        self.attack_damage = 5

    def TakeDamage(self, damage):
        # Take Damage
        self.current_health -= damage

        if self.current_health <= 0:
            # Player has died
            self.current_health = 0
            self.alive = False

    def Attack(self, game_screen, enemy_list):
        f = pygame.draw.rect(game_screen, (0, 0, 255), (self.rect.x - 50, self.rect.y, 100, 50))
        for enemy in enemy_list:
            if f.collidepoint(enemy.rect.x, enemy.rect.y):
                enemy.TakeDamage(self.attack_damage)

    def UpdateAnimation(self, time):
        if self.current_animation.needsUpdate(time):
            self.image = self.current_animation.update()

    def Jump(self):
        upward_speed = -8.0
        if self.can_jump:
            self.y_speed = upward_speed
            self.can_jump = False

    def UpdateMovement(self, collisions):
        move_x, move_y = 0.0, self.y_speed

        if self.moving_right:
            move_x += self.speed
        if self.moving_left:
            move_x -= self.speed

        if move_x > 0.0 and self.current_animation != self.walking_right_animation:
            self.current_animation = self.walking_right_animation
            self.last_direction = "right"
        elif move_x < 0.0 and self.current_animation != self.walking_left_animation:
            self.current_animation = self.walking_left_animation
            self.last_direction = "left"
        elif (move_x == 0.0) and (
                        self.current_animation != self.idle_right_animation or self.current_animation != self.idle_left_animation):
            if self.last_direction == "right":
                self.current_animation = self.idle_right_animation
            elif self.last_direction == "left":
                self.current_animation = self.idle_left_animation

        self.UpdateCollisions(move_x, move_y, collisions)
        self.y_speed += 0.3

    def UpdateCollisions(self, x_movement, y_movement, collisions):
        self.rect.x += x_movement
        collision_list = pygame.sprite.spritecollide(self, collisions, False)
        for collision_object in collision_list:
            if x_movement > 0.0:
                self.rect.right = collision_object.rect.left
            elif x_movement < 0.0:
                self.rect.left = collision_object.rect.right

        self.rect.y += y_movement
        collision_list = pygame.sprite.spritecollide(self, collisions, False)
        for collision_object in collision_list:
            if y_movement > 0.0:
                self.rect.bottom = collision_object.rect.top
                self.y_speed = 0
                self.can_jump = True
            elif y_movement < 0.0:
                self.rect.top = collision_object.rect.bottom
                self.y_speed = 0

    def Update(self, time, collisions_for_player):
        if self.alive:
            self.UpdateMovement(collisions_for_player)
            self.UpdateAnimation(time)


player = Player()

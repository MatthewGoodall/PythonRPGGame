import pygame
import Animation
import CollisionObject
from Enemy import *
from Camera import *
from NPC import *
from JSON_Reader import *

pygame.mixer.init()
pygame.display.init()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.current_health = 10
        self.attack_damage = 5

        self.idle_right_animation = Animation.player_idle_right
        self.idle_left_animation = Animation.player_idle_left
        self.walking_right_animation = Animation.player_walking_right
        self.walking_left_animation = Animation.player_walking_left
        self.current_animation = self.idle_right_animation

        self.image = self.current_animation.get_first_frame()

        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 0

        self.alive = True
        self.speed = 5.0
        self.y_speed = 0.0
        self.jump_pressed = False
        self.moving_up = False
        self.moving_right = False
        self.moving_down = False
        self.moving_left = False
        self.on_ladder = False
        self.touching_ground = True
        self.can_jump = True
        self.last_direction = "right"

        self.items = []

    def TakeDamage(self, damage):
        # Take Damage
        self.current_health -= damage

        if self.current_health <= 0:
            # Player has died
            self.current_health = 0
            self.alive = False

    def Attack(self, game_screen, enemy_list):
        f = None
        player_rect = camera.Apply(self)
        if self.last_direction == "right":
            f = pygame.draw.rect(game_screen, (0, 0, 255),
                                 (self.rect.x, self.rect.y, 100 + self.rect.width, self.rect.height))
        elif self.last_direction == "left":
            f = pygame.draw.rect(game_screen, (0, 0, 255), (
                self.rect.x - 100 - self.rect.width, self.rect.y, 100 + self.rect.width, self.rect.height))
            f = pygame.draw.rect(game_screen, (0, 0, 255),
                                 (player_rect.x, player_rect.y, 100 + player_rect.width, player_rect.height))
        elif self.last_direction == "left":
            f = pygame.draw.rect(game_screen, (0, 0, 255), (
                player_rect.x - 100 - player_rect.width, player_rect.y, 100 + player_rect.width, player_rect.height))
        for enemy in enemy_list:
            enemy_rect = camera.Apply(enemy)
            rects_colliding = f.colliderect(enemy_rect)
            if rects_colliding:
                enemy.TakeDamage(self.attack_damage)
                if not enemy.alive:
                    self.items.append(enemy.typeOfReward)

    def UpdateAnimation(self, time):
        if self.current_animation.needsUpdate(time):
            self.image = self.current_animation.update()

    def ChangeCurrentAnimation(self, new_animation):
        if self.current_animation != new_animation:
            self.current_animation = new_animation

    def Jump(self):
        upward_speed = -8.0
        if self.can_jump:
            self.y_speed = upward_speed
            self.can_jump = False

    def UpdateMovement(self, ground=[], platforms=[], ladders=[]):
        move_x, move_y = 0.0, self.y_speed

        if self.moving_right:
            move_x += self.speed
        if self.moving_left:
            move_x -= self.speed

        if move_x > 0.0:
            self.ChangeCurrentAnimation(self.walking_right_animation)
            self.last_direction = "right"
        elif move_x < 0.0:
            self.ChangeCurrentAnimation(self.walking_left_animation)
            self.last_direction = "left"
        elif move_x == 0.0:
            if self.last_direction == "right":
                self.ChangeCurrentAnimation(self.idle_right_animation)
            elif self.last_direction == "left":
                self.ChangeCurrentAnimation(self.idle_left_animation)

        if self.on_ladder:
            move_y = 0.0
            if self.moving_up or self.jump_pressed:
                move_y -= self.speed / 2
            if self.moving_down:
                move_y += self.speed / 2
        else:
            self.y_speed += 0.3
        self.UpdateCollisions(move_x, move_y, ground, platforms, ladders)

    def UpdateCollisions(self, x_movement, y_movement, ground=[], platforms=[], ladders=[]):
        collisions = ground + platforms + ladders

        self.rect.x += x_movement
        collision_list = pygame.sprite.spritecollide(self, collisions, False)

        self.on_ladder = False
        for ladder in ladders:
            if ladder in collision_list:
                self.on_ladder = True

        for collision_object in collision_list:
            if collision_object in ground:
                if x_movement > 0.0:
                    self.rect.right = collision_object.rect.left
                elif x_movement < 0.0:
                    self.rect.left = collision_object.rect.right

        self.rect.y += y_movement
        collision_list = pygame.sprite.spritecollide(self, collisions, False)
        for collision_object in collision_list:
            prob_not_falling_through_floor = False
            if collision_object in platforms:
                if self.rect.bottom > collision_object.rect.bottom:
                    prob_not_falling_through_floor = True
            if collision_object in ladders:
                prob_not_falling_through_floor = True

            if y_movement > 0.0 and not prob_not_falling_through_floor:
                falling_through = False
                if collision_object in platforms:
                    if self.moving_down: falling_through = True
                if not falling_through:
                    self.rect.bottom = collision_object.rect.top
                    self.y_speed = 0
                    self.can_jump = True
            elif y_movement < 0.0:
                if collision_object in ground:
                    self.rect.top = collision_object.rect.bottom
                    self.y_speed = 0
            if collision_object in ladders:
                self.y_speed = 0

    def NPCCollision(self, collision):
        interact = pygame.sprite.spritecollide(self, collision, False)
        if interact:
            JSON_Reader("Resources\JSON Data\JSON_DATA.json")

    def Update(self, time, ground=[], platforms=[], ladders=[]):
        if self.alive:
            self.UpdateMovement(ground, platforms, ladders)
            self.UpdateAnimation(time)


player = Player()

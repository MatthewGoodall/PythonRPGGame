from Player import *
import pygame
import Animation
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, health, damage, location, spawn_x, spawn_y,
                 idle_animation, walking_right_animation, walking_left_animation,
                 walk_loop_distance, min_gold_drop, max_gold_drop, item_drop_name):
        super().__init__()

        self.damage = damage
        self.maximum_health = health
        self.health = self.maximum_health
        self.damage = 1
        self.location = location
        self.item_drop_name = item_drop_name

        self.alive = True

        self.idle_animation = idle_animation
        self.walking_right_animation = walking_right_animation
        self.walking_left_animation = walking_left_animation
        self.current_animation = walking_right_animation

        self.image = self.current_animation.GetFirstFrame()
        self.rect = self.image.get_rect()
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y
        self.rect.x = self.spawn_x
        self.rect.y = self.spawn_y
        self.speed = 2.0
        self.move_x = 0.0
        self.move_y = 0.0

        self.min_gold_drop = min_gold_drop
        self.max_gold_drop = max_gold_drop

        self.walking_direction = "right"
        self.walking_distance = walk_loop_distance


    def ChangeCurrentAnimation(self, new_animation):
        if self.current_animation is not new_animation:
            self.current_animation = new_animation

    def RandomGoldDrop(self):
        gold_drop = random.randrange(self.min_gold_drop, self.max_gold_drop)
        return gold_drop

    def MakeItemDrop(self):
        return None

    def DoDamage(self):
        player.TakeDamage(self.damage)
        return self.damage

    def TakeDamage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.alive = False

    def Respawn(self):
        self.alive = True
        self.health = self.maximum_health
        self.rect.x = self.spawn_x
        self.rect.y = self.spawn_y

    def UpdateAnimation(self, time):
        if self.current_animation.NeedsUpdate(time):
            self.image = self.current_animation.Update()

    def UpdateMovement(self, collisions, player):
        if self.chasing:
            self.ChasePlayer(collisions, player)
        else:
            self.WalkPath(collisions)

    def ChasePlayer(self, collisions, player):
        self.move_x, self.move_y = 0, 0
        # Movement along x direction
        if self.rect.x >= player.rect.x + 2:
            self.move_x -= self.speed
            self.ChangeCurrentAnimation(self.walking_left_animation)
        elif self.rect.x <= player.rect.x - 2:
            self.move_x += self.speed
            self.ChangeCurrentAnimation(self.walking_right_animation)

        self.UpdateCollisions(collisions)

    def WalkPath(self, collisions, speed=1):
        self.move_x, self.move_y = 0, 0
        if self.walking_direction == "right":
            self.move_x += self.speed
            self.ChangeCurrentAnimation(self.walking_right_animation)
        elif self.walking_direction == "left":
            self.move_x -= self.speed
            self.ChangeCurrentAnimation(self.walking_left_animation)

        self.UpdateCollisions(collisions)

        if self.rect.x >= self.spawn_x + self.walking_distance:
            self.walking_direction = "left"
        elif self.rect.x <= self.spawn_x:
            self.walking_direction = "right"

    def UpdateCollisions(self, collisions):
        self.rect.x += self.move_x
        collision_list = pygame.sprite.spritecollide(self, collisions, False)
        for collision_object in collision_list:
            collision_object.HorizontalCollision(self)

        self.rect.y += self.move_y
        collision_list = pygame.sprite.spritecollide(self, collisions, False)
        for collision_object in collision_list:
            collision_object.VerticalCollision(self)

    def HitGround(self):
        pass

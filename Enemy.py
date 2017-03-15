from Player import *
import pygame
import Animation


class Enemy(pygame.sprite.Sprite):
    def __init__(self, health, damage, location, spawn_x, spawn_y, spawn_animation,
                 idle_animation, walkLoop_start, walkLoop_end, min_gold_drop, max_gold_drop,
                 item_drop_name):
        super().__init__()

        self.damage = damage
        self.maximum_health = health
        self.health = self.maximum_health
        self.damage = 1
        self.location = location
        self.item_drop_name = item_drop_name

        self.spawning = True
        self.alive = True

        self.spawn_animation = spawn_animation
        self.idle_animation = idle_animation
        self.current_animation = spawn_animation
        self.image = self.current_animation.GetFirstFrame()
        self.rect = self.image.get_rect()
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y
        self.rect.x = self.spawn_x
        self.rect.y = self.spawn_y

        self.min_gold_drop = min_gold_drop
        self.max_gold_drop = max_gold_drop

        self.donePath = False
        self.walkLoop_start = walkLoop_start
        self.walkLoop_end = walkLoop_end

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
        if self.current_animation.type == "spawning":
            if self.current_animation.current_frame == self.current_animation.number_of_frames - 1:
                self.current_animation.update()
                self.current_animation = self.idle_animation
                self.spawning = False

        if self.current_animation.NeedsUpdate(time):
            self.image = self.current_animation.Update()

    def ChasePlayer(self, collisions, player, speed=1):
        move_x, move_y = 0, 0
        # Movement along x direction
        if self.rect.x > player.rect.x:
            move_x -= speed
        elif self.rect.x < player.rect.x:
            move_x += speed
        # Movement along y direction
        if self.rect.y < player.rect.y:
            move_y += speed
        elif self.rect.y > player.rect.y:
            move_y -= speed

        self.rect.x += move_x
        collision_list = pygame.sprite.spritecollide(self, collisions, False)
        for collision_object in collision_list:
            if move_x > 0:
                self.rect.right = collision_object.rect.left

            elif move_x < 0:
                self.rect.left = collision_object.rect.right

        self.rect.y += move_y
        collision_list = pygame.sprite.spritecollide(self, collisions, False)
        for collision_object in collision_list:
            if move_y > 0:
                self.rect.bottom = collision_object.rect.top
            elif move_y < 0:
                self.rect.top = collision_object.rect.bottom

    def WalkPath(self, speed=1):
            move_x, move_y = 0, 0

            if not self.donePath:
                move_y -= speed
                if self.rect.y <= self.walkLoop_start:
                    self.donePath = True
            elif self.donePath:
                move_y += speed
                if self.rect.y >= self.walkLoop_end:
                    self.donePath = False
            self.rect.y += move_y

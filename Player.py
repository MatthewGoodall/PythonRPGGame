import pygame
import Animation
import CollisionObject
import Location
import Enemy
import Inventory
import Camera
import NPC

pygame.mixer.init()
pygame.display.init()

class Player(pygame.sprite.Sprite):
    def __init__(self, json_data):
        super().__init__()
        self.alive = True
        self.maximum_health = 10
        self.current_health = self.maximum_health
        self.inventory = Inventory.Inventory()

        self.idle_right_animation = json_data.GetAnimation("player_idle_right")
        self.idle_left_animation = json_data.GetAnimation("player_idle_left")
        self.walking_right_animation = json_data.GetAnimation("player_walking_right")
        self.walking_left_animation = json_data.GetAnimation("player_walking_left")
        self.current_animation = self.idle_right_animation

        self.image = self.current_animation.GetFirstFrame()
        self.rect = self.image.get_rect()

        self.movement_speed = 5.0
        self.vertical_speed = 0.0
        self.move_x = 0.0
        self.move_y = 0.0

        self.jump_pressed = False
        self.up_pressed = False
        self.right_pressed = False
        self.down_pressed = False
        self.left_pressed = False

        self.can_jump = False
        self.facing_direction = "right"

    def TakeDamge(self, amount_of_damage):
        self.current_health -= damage
        if self.current_health <= 0:
            self.current_health = 0
            self.alive = False

    def Attack(self, enemies):
        attack_box = pygame.Rect(0, 0, 150, 50) # create a rect that has a width of 150, height of 50
        attack_box.y = self.rect.y

        if self.facing_direction == "right":
            attack_box.x = self.rect.x

        elif self.facing_direction == "left":
            attack_box.x = self.rect.x - (150 - self.rect.width)

        for enemy in enemies:
            if attack_box.colliderect(enemy.rect):
                print("Enemy took damage") # Just until we know for sure that the attack box is in the correct position / is correct size
                enemy.TakeDamage(5) # Amount of damage will eventually be dependent on weapon and stats

    def UpdateAnimation(self, time):
        if self.current_animation.NeedsUpdate(time):
            self.image = self.current_animation.Update()

    def ChangeCurrentAnimation(self, new_animation):
        if self.current_animation != new_animation:
            self.current_animation = new_animation

    def Jump(self):
        if self.can_jump:
            upward_speed = -8.0
            self.vertical_speed = upward_speed
            self.can_jump = False

    def UpdateMovement(self, current_location):
        # Horizontal Movement
        self.move_x = 0.0
        if self.right_pressed:
            self.move_x += self.movement_speed
        if self.left_pressed:
            self.move_x -= self.movement_speed

        if self.move_x > 0.0:  # Moving right
            self.ChangeCurrentAnimation(self.walking_right_animation)
            self.facing_direction = "right"
        elif self.move_x < 0.0:  # Moving left
            self.ChangeCurrentAnimation(self.walking_left_animation)
            self.facing_direction = "left"
        elif self.move_x == 0.0:  # Standing still
            if self.facing_direction == "right":
                self.ChangeCurrentAnimation(self.idle_right_animation)
            elif self.facing_direction == "left":
                self.ChangeCurrentAnimation(self.idle_left_animation)

        # Vertical Movement
        if not self.CheckForLadderMovement(current_location):
            self.UpdateGravity()

        self.UpdateCollisions(current_location)

    def CheckForLadderMovement(self, current_location):
        ladder_collisions = pygame.sprite.spritecollide(self, current_location.ladders, False)
        if ladder_collisions:
            self.move_y = 0.0
            if self.jump_pressed or self.up_pressed:
                self.move_y -= self.movement_speed/2
            if self.down_pressed:
                self.move_y += self.movement_speed/2
            return True

    def UpdateGravity(self):
        if self.vertical_speed <= 10.0:
            self.vertical_speed += 0.3
        self.move_y = self.vertical_speed

    def HitGround(self):
        self.can_jump = True
        self.vertical_speed = 0.0

    def UpdateCollisions(self, current_location):
        self.rect.x += self.move_x
        collision_list = pygame.sprite.spritecollide(self, current_location.collisions, False)
        for collision_object in collision_list:
            collision_object.HorizontalCollision(self)

        self.rect.y += self.move_y
        collision_list = pygame.sprite.spritecollide(self, current_location.collisions, False)
        for collision_object in collision_list:
            collision_object.VerticalCollision(self)

    def NPCCollision(self, current_location):
        interacts = pygame.sprite.spritecollide(self, current_location.NPCs, False)
        for npc in interacts:
            print(npc.dialogue)

    def GatewayCollision(self, current_location):
        interacts = pygame.sprite.spritecollide(self, current_location.gateways, False)
        for gateway in interacts:
            return gateway

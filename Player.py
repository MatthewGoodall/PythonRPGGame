import pygame
import Animation
import CollisionObject
import Location
import Enemy
import Camera
import NPC
import JSON_Reader

pygame.mixer.init()
pygame.display.init()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.current_health = 10
        self.attack_damage = 5

        self.idle_right_animation = None
        self.idle_left_animation = None
        self.walking_right_animation = None
        self.walking_left_animation = None
        self.current_animation = None

        self.image = None

        self.rect = None

        self.alive = True
        self.speed = 5.0
        self.y_speed = 0.0
        self.up_pressed = False
        self.jump_pressed = False
        self.right_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.on_ladder = False
        self.touching_ground = True
        self.can_jump = True
        self.last_direction = "right"

        self.items = []

    def Load(self):
        self.current_animation = self.idle_right_animation
        self.current_image = self.current_animation
        self.image = self.current_image.GetFirstFrame()
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 0
    def TakeDamage(self, damage):
        # Take Damage
        self.current_health -= damage

        if self.current_health <= 0:
            # Player has died
            self.current_health = 0
            self.alive = False

    def Attack(self, game_screen, camera):
        f = None
        player_rect = camera.Apply(self)
        if self.last_direction == "right":
            f = pygame.draw.rect(game_screen, (0, 0, 255),
                                 (player_rect.x, player_rect.y, 100 + player_rect.width, player_rect.height))
        elif self.last_direction == "left":
            f = pygame.draw.rect(game_screen, (0, 0, 255), (
                player_rect.x - 100 - player_rect.width, player_rect.y, 100 + player_rect.width, player_rect.height))
        for enemy in Level.current_level.enemies:
            enemy_rect = camera.Apply(enemy)
            rects_colliding = f.colliderect(enemy_rect)
            if rects_colliding:
                enemy.TakeDamage(self.attack_damage)
                print("enemy took damage")
                if not enemy.alive:
                    self.items.append(enemy.typeOfReward)

    def UpdateAnimation(self, time):
        if self.current_animation.NeedsUpdate(time):
            self.image = self.current_animation.Update()

    def ChangeCurrentAnimation(self, new_animation):
        if self.current_animation != new_animation:
            self.current_animation = new_animation

    def Jump(self):
        if self.can_jump:
            upward_speed = -8.0
            self.y_speed = upward_speed
            self.can_jump = False

    def UpdateMovement(self, current_location):
        move_x, move_y = 0.0, self.y_speed
        if self.right_pressed:
            move_x += self.speed
        if self.left_pressed:
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
            if self.jump_pressed or self.up_pressed:
                move_y -= self.speed / 2
            if self.down_pressed:
                move_y += self.speed / 2
        else:
            if self.y_speed <= 10.0:
                self.y_speed += 0.3
        self.UpdateCollisions(move_x, move_y, current_location)

    def UpdateCollisions(self, x_movement, y_movement, current_location):
        solids = current_location.solids
        platforms = current_location.platforms
        ladders = current_location.ladders
        collisions = solids + platforms + ladders
        self.rect.x += x_movement
        collision_list = pygame.sprite.spritecollide(self, collisions, False)

        self.on_ladder = False
        for ladder in ladders:
            if ladder in collision_list:
                self.on_ladder = True

        for collision_object in collision_list:
            if collision_object in solids:
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
                    if self.down_pressed: falling_through = True
                if not falling_through:
                    self.rect.bottom = collision_object.rect.top
                    self.y_speed = 0
                    self.can_jump = True
            elif y_movement < 0.0:
                if collision_object in solids:
                    self.rect.top = collision_object.rect.bottom
                    self.y_speed = 0
            if collision_object in ladders:
                self.y_speed = 0.0

    def Interact(self):
        self.NPCCollision()
        self.GatewayCollision()

    def NPCCollision(self):
        interact = pygame.sprite.spritecollide(self, Level.current_level.NPCs, False)
        if interact:
            Read_JSON("Resources\JSON Data\JSON_DATA.json", "Bad Guy", "dialogue")

    def GatewayCollision(self):
        pass

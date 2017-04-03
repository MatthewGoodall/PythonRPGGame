import pygame
import PhysicsSprite
import Animation
import CollisionObject
import Location
import Enemy
import Inventory
import Projectile
import Camera
import NPC
import Item
import copy

pygame.mixer.init()
pygame.display.init()

class Player(PhysicsSprite.PhysicsSprite):
    def __init__(self, json_data):
        super().__init__(json_data.GetAnimation("player_idle_right").GetFirstFrame(), 300, 1200)

        self.alive = True
        self.maximum_health = 10
        self.current_health = self.maximum_health
        self.maximum_mana = 10
        self.current_mana = self.maximum_mana
        self.inventory = Inventory.Inventory()
        self.npc_talking_to = None

        self.Spells = json_data.spells
        self.spell_1 = self.Spells[0]

        self.idle_right_animation = json_data.GetAnimation("player_idle_right")
        self.idle_left_animation = self.idle_right_animation.GetMirrorAnimation()
        self.walking_right_animation = json_data.GetAnimation("player_walking_right")
        self.walking_left_animation = self.walking_right_animation.GetMirrorAnimation()
        self.attacking_left_animation = json_data.GetAnimation("player_attacking_left")
        self.attacking_right_animation = self.attacking_left_animation.GetMirrorAnimation()
        self.current_animation = self.idle_right_animation
        self.attacking = False
        self.make_attack = False


        self.jump_pressed = False
        self.up_pressed = False
        self.right_pressed = False
        self.down_pressed = False
        self.left_pressed = False

        self.can_jump = False
        self.movement_speed = 5.0

    def ChangeCurrentAnimation(self, new_animation):
        if self.current_animation is not new_animation:
            self.current_animation = new_animation

    def UpdateAnimation(self, time):
        if self.current_animation.NeedsUpdate(time):
            if self.current_animation == self.attacking_right_animation:
                if self.current_animation.current_frame == self.current_animation.number_of_frames - 1:
                    self.attacking = False
                    self.current_animation.current_frame = 0
                    return  # Dont update animation
            elif self.current_animation == self.attacking_left_animation:
                if self.current_animation.current_frame == self.current_animation.number_of_frames - 1:
                    self.attacking = False
                    self.current_animation.current_frame = 0
                    return  # Dont update animation

            self.image = self.current_animation.Update()

    def UpdateAttacks(self, enemies):
        if self.make_attack and self.attacking:
            if self.current_animation.current_frame == 3:
                self.MakeMeleeAttack(enemies)
                self.make_attack = False

    def TakeDamge(self, amount_of_damage):
        self.current_health -= damage
        if self.current_health <= 0:
            self.current_health = 0
            self.alive = False

    def CastSpell(self, projectile_list):
        spell_cast = Projectile.Projectile(self.spell_1, 0, 0)
        spell_cast.rect.y = self.rect.centery - spell_cast.rect.height/2
        if self.FacingLeft():
            spell_cast.UpdateDirection("left")
            spell_cast.rect.x = self.rect.left
        elif self.FacingRight():
            spell_cast.UpdateDirection("right")
            spell_cast.rect.x = self.rect.right

        projectile_list.append(spell_cast)
        self.current_mana -= 1

    def MeleeAttack(self, enemies):
        if not self.attacking:
            self.attacking = True
            self.make_attack = True
            if self.FacingRight():
                self.ChangeCurrentAnimation(self.attacking_right_animation)
            elif self.FacingLeft():
                self.ChangeCurrentAnimation(self.attacking_left_animation)

    def MakeMeleeAttack(self, enemies):
        attack_box = pygame.Rect(0, 0, 150, 50) # create a rect that has a width of 150, height of 50
        attack_box.y = self.rect.y

        if self.FacingRight():
            attack_box.x = self.rect.x
        elif self.FacingLeft():
            attack_box.x = self.rect.x - (150 - self.rect.width)

        for enemy in enemies:
            if attack_box.colliderect(enemy.rect):
                enemy.TakeDamage(5) # Amount of damage will eventually be dependent on weapon and stats

    def Jump(self):
        if self.can_jump:
            upward_speed = -10.0
            self.y_velocity = upward_speed
            self.can_jump = False

    def UpdateMovement(self, current_location):
        # Horizontal Movement
        self.move_x = 0.0

        if self.right_pressed:
            self.move_x += self.movement_speed
        if self.left_pressed:
            self.move_x -= self.movement_speed

        if self.move_x > 0.0:  # Moving right
            if not self.attacking:
                self.ChangeCurrentAnimation(self.walking_right_animation)
            self.UpdateXDirection("right")

        elif self.move_x < 0.0:  # Moving left
            if not self.attacking:
                self.ChangeCurrentAnimation(self.walking_left_animation)
            self.UpdateXDirection("left")

        elif self.move_x == 0.0:  # Standing still
            if self.FacingRight() and not self.attacking:
                self.ChangeCurrentAnimation(self.idle_right_animation)
            elif self.FacingLeft() and not self.attacking:
                self.ChangeCurrentAnimation(self.idle_left_animation)

        # Vertical Movement
        self.move_y = 0.0
        if not self.CheckForLadderMovement(current_location):
            self.ApplyGravity()

        # Check for leaving npc range
        self.NPCCollision(current_location)
        # Update collisions
        self.ApplyCollisions(current_location)

    def CheckForLadderMovement(self, current_location):
        ladder_collisions = pygame.sprite.spritecollide(self, current_location.ladders, False)
        if ladder_collisions:
            for ladder in ladder_collisions:
                if ladder.rect.bottom > self.rect.centery:
                    self.y_velocity = 0.0
                    self.move_y = 0.0
                    if self.jump_pressed or self.up_pressed:
                        self.move_y -= self.movement_speed/2
                    if self.down_pressed:
                        self.move_y += self.movement_speed/2
                    return True
        return False

    def HitGround(self):
        super().HitGround()
        self.can_jump = True

    def NPCCollision(self, current_location):
        interacts = pygame.sprite.spritecollide(self, current_location.NPCs, False)
        for npc in interacts:
            self.npc_talking_to = npc
        if not interacts:
            self.npc_talking_to = None

    def GatewayCollision(self, current_location):
        interacts = pygame.sprite.spritecollide(self, current_location.gateways, False)
        for gateway in interacts:
            return gateway

    def ItemDropCollision(self, current_location):
        interacts = pygame.sprite.spritecollide(self, current_location.item_drops, False)
        for item_drop in interacts:
            if isinstance(item_drop, Item.GoldDrop):
                self.inventory.AddGold(item_drop.value)
            else:
                self.inventory.AddItem(item_drop.item)
            current_location.item_drops.remove(item_drop)

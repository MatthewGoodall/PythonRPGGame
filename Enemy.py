import PhysicsSprite
import Animation
import random

class Enemy(PhysicsSprite.PhysicsSprite):
    def __init__(self, json_data, enemy_data, index):
        super().__init__(json_data.GetAnimation(enemy_data[index]["idle animation"]).GetFirstFrame(),
                         int( enemy_data[index]["spawn x"]), int( enemy_data[index]["spawn y"] ))

        self.idle_animation = json_data.GetAnimation(enemy_data[index]["idle animation"])
        self.walking_right_animation = json_data.GetAnimation(enemy_data[index]["walking right animation"])
        self.walking_left_animation = self.walking_right_animation.GetMirrorAnimation()
        self.current_animation = self.idle_animation
        self.damage = int( enemy_data[index]["damage"] )
        self.maximum_health = int( enemy_data[index]["health"] )
        self.health = self.maximum_health
        self.location = enemy_data[index]["location name"]
        self.speed = 3.0
        self.alive = True

        self.spawn_x = self.rect.x
        self.spawn_y = self.rect.y
        self.walkloop_distance = int( enemy_data[index]["walkloop distance"] )
        self.UpdateXDirection("right")

        self.min_gold_drop = int( enemy_data[index]["min gold drop"] )
        self.max_gold_drop = int( enemy_data[index]["max gold drop"] )
        self.item_drop_name = enemy_data[index]["item drop name"]
        self.item_drop = None

    def ChangeCurrentAnimation(self, new_animation):
        if self.current_animation is not new_animation:
            self.current_animation = new_animation

    def UpdateAnimation(self, time):
        if self.move_x > 0:
            self.ChangeCurrentAnimation(self.walking_right_animation)
        elif self.move_x < 0:
            self.ChangeCurrentAnimation(self.walking_left_animation)

        if self.current_animation.NeedsUpdate(time):
            self.image = self.current_animation.Update()

    def RandomGoldDrop(self):
        gold_drop = random.randrange(self.min_gold_drop, self.max_gold_drop)
        return gold_drop

    def RandomLootDrop(self):
        roll = random.randrange(0, 100)
        if roll >= 0:
            return self.item_drop
    def DoDamage(self):
        pass

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

    def UpdateMovement(self, current_location, player):
        if abs(player.rect.centerx - self.rect.centerx) < 300.0:
            self.ChasePlayer(current_location, player)
        else:
            self.WalkPath(current_location)

    def ChasePlayer(self, current_location, player):
        self.move_x, self.move_y = 0, 0
        # Movement along x direction
        if self.rect.x > player.rect.x + 2:
            self.move_x -= self.speed
            self.UpdateXDirection("left")
        elif self.rect.x < player.rect.x - 2:
            self.move_x += self.speed
            self.UpdateXDirection("right")

        self.ApplyGravity()
        self.ApplyCollisions(current_location)


    def WalkPath(self, current_location):
        self.move_x, self.move_y = 0, 0
        if self.rect.x < self.spawn_x:
            self.UpdateXDirection("right")
        elif self.rect.x > self.spawn_x + self.walkloop_distance:
            self.UpdateXDirection("left")

        if self.FacingRight():
            self.move_x += self.speed -1
        elif self.FacingLeft():
            self.move_x -= self.speed -1
        self.ApplyGravity()
        self.ApplyCollisions(current_location)

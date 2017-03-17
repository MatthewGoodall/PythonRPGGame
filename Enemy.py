import PhysicsSprite
import Animation
import random

class Enemy(PhysicsSprite.PhysicsSprite):
    def __init__(self, json_data, enemy_data, index):
        self.idle_right_animation = json_data.GetAnimation(enemy_data[index]["idle animation"])
        starting_x = int( enemy_data[index]["spawn x"] )
        starting_y = int( enemy_data[index]["spawn y"] )
        super().__init__(self.idle_right_animation.GetFirstFrame(), starting_x, starting_y)

        self.current_animation = self.idle_right_animation
        self.damage = int( enemy_data[index]["damage"] )
        self.maximum_health = int( enemy_data[index]["health"] )
        self.health = self.maximum_health
        self.location = enemy_data[index]["location name"]

        self.alive = True

        self.spawn_x = self.rect.x
        self.spawn_y = self.rect.y

        self.min_gold_drop = int( enemy_data[index]["min gold drop"] )
        self.max_gold_drop = int( enemy_data[index]["max gold drop"] )
        self.item_drop_name = enemy_data[index]["item drop name"]
        self.item_drop = None

    def ChangeCurrentAnimation(self, new_animation):
        if self.current_animation is not new_animation:
            self.current_animation = new_animation

    def UpdateAnimation(self, time):
        if self.current_animation.NeedsUpdate(time):
            self.image = self.current_animation.Update()

    def RandomGoldDrop(self):
        gold_drop = random.randrange(self.min_gold_drop, self.max_gold_drop)
        return gold_drop

    def RandomLootDrop(self):
        roll = random.randrange(0, 100)
        if roll >= 75:
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

    def WalkPath(self, speed=1):
        pass

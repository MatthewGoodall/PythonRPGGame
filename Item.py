import pygame

class Item():
  def __init__(self, item_name, image_path, gold_value):
    self.image = pygame.image.load(image_path).convert_alpha()
    self.rect = self.image.get_rect()
    self.name = item_name
    self.value = gold_value

class ItemDrop(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.y_speed = 0.0
        self.move_y = 0.0

    def Update(self, collisions):
        self.move_y = self.y_speed
        self.rect.y += self.move_y
        collision_list = pygame.sprite.spritecollide(self, collisions, False)
        for collision_object in collision_list:
            if self.move_y > 0:
                collision_object.VerticalCollision(self)

        self.y_speed += 0.3

    def HitGround(self):
        self.y_speed = 0.0

class NormalItemDrop(ItemDrop):
    def __init__(self, item, x, y):
        super().__init__(item.image, x, y)
        self.item = item

class GoldDrop(ItemDrop):
    def __init__(self, gold_value, x, y):
        gold_picture = pygame.image.load("Resources/SinglePhotos/Gold.png").convert_alpha()
        super().__init__(gold_picture, x, y)
        self.value = gold_value

class Weapon(Item):
  def __init__(self, weapon_name, image_path, gold_value, weapon_damage):
    super().__init__(weapon_name, image_path, gold_value)
    self.damage = weapon_damage

class Potion(Item):
  def __init__(self, potion_name, image_path, gold_value):
    super().__init__(potion_name, image_path, gold_value)

class RestorePotion(Potion):
  def __init__(self, potion_name, image_path, gold_value, heal_amount, mana_restore_value):
    super().__init__(potion_name, image_path, gold_value)

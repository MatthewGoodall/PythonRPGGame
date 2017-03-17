import pygame
import PhysicsSprite

class Item():
  def __init__(self, item_data, index):
    self.image = pygame.image.load(item_data[index]["image path"]).convert_alpha()
    self.rect = self.image.get_rect()
    self.name = item_data[index]["name"]
    self.value = item_data[index]["gold value"]

class ItemDrop(PhysicsSprite.PhysicsSprite):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)

    def Update(self, current_location):
        self.ApplyGravity()
        self.ApplyCollisions(current_location)
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
  def __init__(self, weapon_data, index):
    super().__init__(weapon_data, index)
    self.damage = weapon_data[index]["damage"]

class Potion(Item):
  def __init__(self, potion_data, index):
    super().__init__(potion_data, index)

class RestorePotion(Potion):
  def __init__(self, restore_potion_data, index):
    super().__init__(restore_potion_data, index)
    self.restore_amount = restore_potion_data[index]["mana restore value"]

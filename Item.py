import pygame
       
class Item():
  def __init__(self, item_name, gold_value):
    self.name = item_name
    self.value = gold_value
    
class Weapon(Item):
  def __init__(self, weapon_name, gold_value, weapon_damage):
    super().__init__(weapon_name, gold_value)
    self.damage = weapon_damage
    
class Potion(Item):
  def __init__(self, potion_name, gold_value):
    super().__init__(potion_name, gold_value)
    
class HealingPotion(Potion):
  def __init__(self, potion_name, gold_value, heal_amount):
    super().__init__(potion_name, gold_value)
    
#Create Items
sword = Weapon("Excaliber", 5, 7)
health = HealingPotion("Health Potion", 5, 10)
    
"""
class Item():

def __init__(self):

def Weapon(self, damage, worth, name, weaponType):

def Potion(self, worth, potionType, description, name, doesDamage = false):

def Misc(self):
"""

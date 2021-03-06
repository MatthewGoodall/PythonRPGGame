import pygame
class Spell(pygame.sprite.Sprite):
    def __init__(self, spell_data, index):
        super().__init__()
        self.image = pygame.image.load(spell_data[index]["image path"]).convert_alpha()
        self.rect = self.image.get_rect()
        self.name = spell_data[index]["name"]

class DamageSpell(Spell):
    def __init__(self, spell_data, index, json_data):
        super().__init__(spell_data, index)
        self.spell = spell_data[index]["name"]
        self.damage = int( spell_data[index]["damage"] )
        self.image_path = spell_data[index]["image path"]
        self.animation = json_data.GetAnimation(spell_data[index]["animation name"])
        self.effect = spell_data[index]["effect"]
        self.speed = 6.0

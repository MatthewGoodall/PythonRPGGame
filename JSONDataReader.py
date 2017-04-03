import json
import NPC
import Enemy
import Animation
import Location
import Item
import Spells

class JSONDataReader:
    def __init__(self):
        self.NPCs = []
        self.animations = []
        self.enemies = []
        self.locations = []
        self.weapons = []
        self.spells = []
        self.healing_potions = []

        self.bad_characters = '{}[]""'

    def MakeWeapon(self, file_path):
        with open(file_path) as data_file:
            data = json.load(data_file)
            for weapon in data:
                a_weapon = Item.Weapon(data, weapon)
                self.weapons.append(a_weapon)

    def MakeDamageSpell(self, file_path):
        with open(file_path) as data_file:
            data = json.load(data_file)
            for spell in data:
                a_spell = Spells.DamageSpell(data, spell, self)
                self.spells.append(a_spell)

    def MakePotion(self, file_path):
        with open(file_path) as data_file:
            data = json.load(data_file)
            for potion in data:
                a_potion = Item.RestorePotion(data, potion)
                self.healing_potions.append(a_potion)

    def MakeNPCs(self, file_path):
        with open(file_path) as data_file:
            data = json.load(data_file)
            for npc in data:
                a_npc = NPC.NPC(data, npc)
                self.NPCs.append(a_npc)

    def MakeAnimations(self, file_path):
        with open(file_path) as data_file:
            data = json.load(data_file)
            for animation in data:
                an_animation = Animation.Animation(data, animation)
                self.animations.append(an_animation)

    def MakeEnemies(self, file_path):
        # Read JSON data
        # Make enemy from each section of json data
        # Add each enemy to self.Enemies
        with open(file_path) as data_file:
            data = json.load(data_file)
            for enemy in data:
                an_enemy = Enemy.Enemy(self, data, enemy)
                self.enemies.append(an_enemy)

    def MakeLocations(self, file_path):
        with open(file_path) as data_file:
            data = json.load(data_file)
            for location in data:
                name_of_location = data[location]["name"]
                tmx_map_path_of_location = data[location]["tmx map path"]
                a_location = Location.Location(name_of_location, tmx_map_path_of_location)
                self.locations.append(a_location)

    def PopulateLocations(self):
        for enemy in self.enemies:
            for location in self.locations:
                if location.name == enemy.location:
                    location.enemies.append(enemy)
            for item in self.weapons:
                if enemy.item_drop_name == item.name:
                    enemy.item_drop = item

        for npc in self.NPCs:
            for location in self.locations:
                if location.name == npc.location:
                    location.NPCs.append(npc)

    def GetAnimation(self, animation_name):
        for animation in self.animations:
            if animation.name == animation_name:
                return animation
        print("No animation found with the name of: " + animation_name)

    def GetLocation(self, location_name):
        for location in self.locations:
            if location.name == location_name:
                return location
        print("No location found with the name of: "+ location_name)

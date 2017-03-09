import json


class NPC:
    def __init__(self, name, dialogue):
        self.name = name
        self.dialogue = dialogue


class Enemy:
    def __init__(self, name, damage, location_name, spawn_x, spawn_y):
        self.name = name
        self.damage = damage
        self.location_name = location_name
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y


class JSONDataReader:
    def __init__(self):
        self.NPCs = []
        self.Animations = []
        self.Enemies = []
        self.Locations = []

        self.bad_characters = '{}[]""'

    def MakeNPCs(self, file_path):
        # Read JSON data
        # Make NPC from each section of json data
        # Add each NPC to self.NPCs
        with open(file_path) as data_file:
            data = json.load(data_file)
            for npc in data:
                name_of_npc = data[npc]["name"]
                dialogue_of_npc = data[npc]["dialogue"]
                a_npc = NPC(name_of_npc, dialogue_of_npc)
                self.NPCs.append(a_npc)

    def MakeAnimations(self, file_path):
        # Read JSON data
        # Make animation from each section of json data
        # Add each animation to self.Animations
        pass

    def MakeEnemies(self, file_path):
        # Read JSON data
        # Make enemy from each section of json data
        # Add each enemy to self.Enemies
        with open(file_path) as data_file:
            data = json.load(data_file)
            for enemy in data:
                name_of_enemy = data[enemy]["name"]
                damage_of_enemy = data[enemy]["damage"]
                location_of_enemy = data[enemy]["location_name"]
                spawn_x_of_enemy = data[enemy]["spawn_x"]
                spawn_y_of_enemy = data[enemy]["spawn_y"]
                a_enemy = Enemy(name_of_enemy, damage_of_enemy, location_of_enemy, spawn_x_of_enemy, spawn_y_of_enemy)
                self.Enemies.append(a_enemy)

    def MakeLocations(self, file_path):
        # Read JSON data
        # Make location from each section of json data
        # Add each location to self.Locations
        pass

    def PopulateLocations(self):
        """
        For enemy in self.enemies:
            for location in self.locations:
                if location.name == enemy.location_name
                    location.enemies.append(enemy)

        for npc in self.NPCs:
            for location in self.locations:
                if location.name == enemy.location_name
                    location.enemies.append(enemy)
        """

    def GetAnimation(self, animation_name):
        """
        for animation in self.Animations:
            if animation.name == animation_name
                return animation
        print("No animation found with the name of: " + animation_name)
        """


json_reader = JSONDataReader()
json_reader.MakeNPCs("Resources/JSON Data/NPC_DATA.json")

for poop in json_reader.NPCs:
    print(poop.name)

json_reader.MakeEnemies("Resources/JSON Data/ENEMY_DATA.json")
for poops in json_reader.Enemies:
    print(poops.name)

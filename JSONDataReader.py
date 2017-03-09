import json

class NPC:
    def __init__(self, name, dialogue):
        self.name = name
        self.dialogue = dialogue

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
        pass
        # Read JSON data
        # Make enemy from each section of json data
        # Add each enemy to self.Enemies

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
json_reader.MakeNPCs("Resources/JSON Data/JSON_DATA.json")
for npc in json_reader.NPCs:
    print(npc.name)

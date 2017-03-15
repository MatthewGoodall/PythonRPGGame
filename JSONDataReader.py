import json
import NPC
import Enemy
import Animation
import Location
import Item

class JSONDataReader:
    def __init__(self):
        self.NPCs = []
        self.animations = []
        self.enemies = []
        self.locations = []
        self.weapons = []
        self.healing_potions = []

        self.bad_characters = '{}[]""'

    def MakeWeapon(self, file_path):
        with open(file_path) as data_file:
            data = json.load(data_file)
            for weapon in data:
                damage = data[weapon]["damage"]
                name = data[weapon]["name"]
                image_path = data[weapon]["image_path"]
                gold_value = data[weapon]["gold_value"]
                a_weapon = Item.Weapon(name, image_path, gold_value, damage)
                self.weapons.append(a_weapon)


    def MakeHealingPotion(self, file_path):
        with open(file_path) as data_file:
            data = json.load(data_file)
            for potion in data:
                name = data[potion]["name"]
                image_path = data[potion]["image_path"]
                gold_value = data[potion]["gold_value"]
                healing_value = data[potion]["heailing_value"]
                a_potion = Item.HealingPotion(name, image_path, gold_value, healing_value)
                self.healing_potions.append(a_potion)

    def MakeNPCs(self, file_path):
        with open(file_path) as data_file:
            data = json.load(data_file)
            for npc in data:
                name_of_npc = data[npc]["name"]
                location_of_npc = data[npc]["location"]
                image_path_of_npc = data[npc]["image path"]
                x_pos_of_npc = int(data[npc]["x pos"])
                y_pos_of_npc = int(data[npc]["y pos"])
                dialogue_of_npc = data[npc]["dialogue"]
                a_npc = NPC.NPC(name_of_npc, location_of_npc, image_path_of_npc,  x_pos_of_npc, y_pos_of_npc,
                            dialogue_of_npc)
                self.NPCs.append(a_npc)

    def MakeAnimations(self, file_path):
        with open(file_path) as data_file:
            data = json.load(data_file)
            for animation in data:
                name_of_anim = data[animation]["name"]
                type_of_anim = data[animation]["type"]
                spritesheet_path_of_anim = data[animation]["spritesheet path"]
                frame_width_of_anim = int(data[animation]["frame width"])
                frame_height_of_anim = int(data[animation]["frame height"])
                number_of_frames_of_anim = int(data[animation]["number of frames"])
                frame_delay_of_anim = int(data[animation]["frame delay"])
                scale_of_anim = int(data[animation]["scale"])
                an_animation = Animation.Animation(name_of_anim, type_of_anim, spritesheet_path_of_anim,
                                                   frame_width_of_anim, frame_height_of_anim, number_of_frames_of_anim,
                                                   frame_delay_of_anim, scale_of_anim)
                self.animations.append(an_animation)

    def MakeEnemies(self, file_path):
        # Read JSON data
        # Make enemy from each section of json data
        # Add each enemy to self.Enemies
        with open(file_path) as data_file:
            data = json.load(data_file)
            for enemy in data:
                health_of_enemy = int(data[enemy]["health"])
                damage_of_enemy = int(data[enemy]["damage"])
                location_of_enemy = data[enemy]["location_name"]
                spawn_x_of_enemy = int(data[enemy]["spawn x"])
                spawn_y_of_enemy = int(data[enemy]["spawn y"])
                spawn_animation_name = data[enemy]["spawn animation"]
                spawn_animation_of_enemy = self.GetAnimation(spawn_animation_name)
                idle_animation_name = data[enemy]["idle animation"]
                idle_animation_of_enemy = self.GetAnimation(idle_animation_name)
                walkloop_start_of_enemy = int(data[enemy]["walkloop start"])
                walkloop_end_of_enemy = int(data[enemy]["walkloop end"])
                an_enemy = Enemy.Enemy(health_of_enemy, damage_of_enemy, location_of_enemy,
                                 spawn_x_of_enemy, spawn_y_of_enemy, spawn_animation_of_enemy,
                                 idle_animation_of_enemy, walkloop_start_of_enemy, walkloop_end_of_enemy)
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

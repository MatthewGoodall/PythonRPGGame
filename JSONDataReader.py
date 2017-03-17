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


    def MakePotion(self, file_path):
        with open(file_path) as data_file:
            data = json.load(data_file)
            for potion in data:
                name = data[potion]["name"]
                image_path = data[potion]["image_path"]
                gold_value = data[potion]["gold_value"]
                if data[potion]["type"] == "Healing":
                    healing_value = data[potion]["healing_value"]
                else:
                    healing_value = 0
                if data[potion]["type"] == "Mana":
                    mana_restore_value = data[potion]["mana_restore_value"]
                else:
                    mana_restore_value = 0
                a_potion = Item.RestorePotion(name, image_path, gold_value, healing_value, mana_restore_value)
                self.healing_potions.append(a_potion)

    def MakeNPCs(self, file_path):
        with open(file_path) as data_file:
            data = json.load(data_file)
            for npc in data:
                name_of_npc = data[npc]["name"]
                location_of_npc = data[npc]["location"]
                image_path_of_npc = data[npc]["image path"]
                close_up_of_npc = data[npc]["closeup path"]
                x_pos_of_npc = int(data[npc]["x pos"])
                y_pos_of_npc = int(data[npc]["y pos"])
                dialogue_of_npc = data[npc]["dialogue"]
                a_npc = NPC.NPC(name_of_npc, location_of_npc, image_path_of_npc,  close_up_of_npc,
                                x_pos_of_npc, y_pos_of_npc, dialogue_of_npc)
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

                item_drop_name = data[enemy]["item_drop_name"]

                idle_animation_name = data[enemy]["idle animation"]
                idle_animation_of_enemy = self.GetAnimation(idle_animation_name)

                walking_right_animation_name = data[enemy]["walking right animation"]
                walking_right_animation_of_enemy = self.GetAnimation(walking_right_animation_name)

                walking_left_animation_name = data[enemy]["walking left animation"]
                walking_left_animation_of_enemy = self.GetAnimation(walking_left_animation_name)

                walk_loop_distance_of_enemy = int(data[enemy]["walkloop distance"])

                min_gold_drop = int(data[enemy]["min gold drop"])
                max_gold_drop = int(data[enemy]["max gold drop"])

                an_enemy = Enemy.Enemy(health_of_enemy, damage_of_enemy, location_of_enemy,
                                 spawn_x_of_enemy, spawn_y_of_enemy,
                                 idle_animation_of_enemy, walking_right_animation_of_enemy,
                                 walking_left_animation_of_enemy, walk_loop_distance_of_enemy,
                                 min_gold_drop, max_gold_drop, item_drop_name)
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

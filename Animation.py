import pygame


class Animation:
    def __init__(self, sprite_sheet_path, frame_width, frame_height, number_of_frames, scale, height=0):
        self.type = ""
        self.current_frame = 0
        self.time_counter = 0.0
        self.ms_delay = 500
        self.frame_width = frame_width * scale
        self.frame_height = frame_height * scale
        self.frames = []
        self.height = height
        self.sprite_sheet = pygame.image.load(sprite_sheet_path)
        if scale > 1:
            self.sprite_sheet = pygame.transform.scale(self.sprite_sheet,
                                                       (self.sprite_sheet.get_width() * scale, self.frame_height))

        self.number_of_frames = number_of_frames
        for i in range(self.number_of_frames):
            new_image = self.sprite_sheet.subsurface(
                (i * self.frame_width, self.height, self.frame_width, self.frame_height))
            self.frames.append(new_image)

    def get_first_frame(self):
        frame_1 = self.sprite_sheet.subsurface((0, self.height, self.frame_width, self.frame_height))
        return frame_1

    def needsUpdate(self, current_time):
        if current_time - self.time_counter > self.ms_delay:
            self.time_counter = current_time
            return True
        else:
            return False

    def update(self):
        self.current_frame += 1
        if self.current_frame > self.number_of_frames - 1:
            self.current_frame = 0
        image_to_return = self.frames[self.current_frame]
        return image_to_return


# name_of_animation = Animation("File path", frame_w, frame_h, # of frames, (scale)
# ms delay defaults to 500ms
player_walking_right = Animation("Resources/Spritesheets/PlayerWalkingRight.png", 8, 16, 4, 4)
player_walking_right.ms_delay = 125
player_walking_left = Animation("Resources/Spritesheets/PlayerWalkingLeft.png", 8, 16, 4, 4)
player_walking_left.ms_delay = 125
player_idle_right = Animation("Resources/Spritesheets/PlayerIdleRight.png", 8, 16, 2, 4)
player_idle_left = Animation("Resources/Spritesheets/PlayerIdleLeft.png", 8, 16, 2, 4)

squid_spawning = Animation("Resources/Spritesheets/Squid.png", 19, 23, 1, 1)
squid_spawning.type = "spawning"
squid_idle = Animation("Resources/SinglePhotos/Squid.png", 19, 23, 1, 1)

dragon_idle = Animation("Resources/Spritesheets/DragonLeft.png", 20, 20, 1, 8)
dragon_spawning = Animation("Resources/Spritesheets/DragonLeft.png", 20, 20, 1, 8)
dragon_spawning.type = "spawning"

hen_idle = Animation("Resources/Spritesheets/Henrey.png", 18, 18, 1, 1)
hen_spawning = Animation("Resources/Spritesheets/Henrey.png", 18, 18, 1, 1)
hen_spawning.type = "spawning"

health_bar_anim = Animation("Resources/Spritesheets/HealthBar.png", 66, 66, 2, 3)
mana_bar_anim = Animation("Resources/Spritesheets/ManaBar.png", 66, 66, 1, 3)

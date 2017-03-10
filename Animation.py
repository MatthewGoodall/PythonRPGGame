import pygame


class Animation:
    def __init__(self, name, type_of_animation,spritesheet_path, frame_width, frame_height,
                 number_of_frames, frame_delay, scale, height=0):
        self.name = name
        self.type = type_of_animation
        self.current_frame = 0
        self.time_counter = 0.0
        self.ms_delay = frame_delay
        self.frame_width = frame_width * scale
        self.frame_height = frame_height * scale
        self.frames = []
        self.height = height
        self.sprite_sheet = pygame.image.load(spritesheet_path)
        if scale > 1:
            self.sprite_sheet = pygame.transform.scale(self.sprite_sheet,
                                                       (self.sprite_sheet.get_width() * scale,
                                                        self.frame_height))

        self.number_of_frames = number_of_frames
        for i in range(self.number_of_frames):
            new_image = self.sprite_sheet.subsurface(
                (i * self.frame_width, self.height, self.frame_width, self.frame_height))
            self.frames.append(new_image)

    def GetFirstFrame(self):
        frame_1 = self.sprite_sheet.subsurface((0, self.height, self.frame_width, self.frame_height))
        return frame_1

    def NeedsUpdate(self, current_time):
        if current_time - self.time_counter > self.ms_delay:
            self.time_counter = current_time
            return True
        else:
            return False

    def Update(self):
        self.current_frame += 1
        if self.current_frame > self.number_of_frames - 1:
            self.current_frame = 0
        image_to_return = self.frames[self.current_frame]
        return image_to_return

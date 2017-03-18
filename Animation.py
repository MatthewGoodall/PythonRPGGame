import pygame


class Animation:
    def __init__(self, animation_data, index):
        self.name = animation_data[index]["name"]

        self.spritesheet = pygame.image.load(animation_data[index]["spritesheet path"]).convert_alpha()
        scale = int( animation_data[index]["scale"] )
        self.spritesheet = pygame.transform.scale(self.spritesheet, (self.spritesheet.get_width()*scale, self.spritesheet.get_height()*scale))

        self.current_frame = 0
        self.time_counter = 0.0
        self.ms_delay = int( animation_data[index]["frame delay"] )

        self.number_of_frames =int( animation_data[index]["number of frames"] )
        self.frame_width = self.spritesheet.get_width() / self.number_of_frames
        self.frame_height = self.spritesheet.get_height()

        self.frames = []
        self.start_height = int( animation_data[index]["start height"] )

        for i in range(self.number_of_frames):
            new_image = self.spritesheet.subsurface(
                (i * self.frame_width, self.start_height, self.frame_width, self.frame_height))
            self.frames.append(new_image)

    def GetFirstFrame(self):
        return self.frames[0]

    def GetFrame(self, n):
        return self.frames[n]

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

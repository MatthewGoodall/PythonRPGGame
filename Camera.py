import pygame


class Camera(pygame.sprite.Sprite):
    def __init__(self, width_of_level, height_of_level, width_of_screen, height_of_screen):
        self.rect = pygame.Rect(0, 0, width_of_level, height_of_level)
        self.screen_width = width_of_screen
        self.half_screen_width = self.screen_width / 2
        self.screen_height = height_of_screen
        self.half_screen_height = self.screen_height / 2

    def ApplyToSprite(self, target_sprite):
        return target_sprite.rect.move(self.rect.topleft)

    def ApplyToRect(self, target_rect):
        return target_rect.move(self.rect.topleft)

    def ChangeLocationSize(self, new_width, new_height):
        self.rect.width = new_width
        self.rect.height = new_height

    def Update(self, target):
        self.rect = self.ApplyCamera(target.rect)

    def ApplyCamera(self, target_rect):

        l, t, _, _ = target_rect
        _, _, w, h = self.rect
        l, t, _, _ = -l + self.half_screen_width, -t + self.half_screen_height, w, h

        l = min(0, l)
        l = max(-(self.rect.width - self.screen_width), l)
        t = max(-(self.rect.height - self.screen_height), t)
        t = min(0, t)
        return pygame.Rect(l, t, w, h)

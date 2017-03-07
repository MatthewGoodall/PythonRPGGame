import pygame


class Camera(pygame.sprite.Sprite):
    def __init__(self, width_of_level, height_of_level):
        self.rect = pygame.Rect(0, 0, width_of_level, height_of_level)

    def ApplyToSprite(self, target_sprite):
        return target_sprite.rect.move(self.rect.topleft)

    def ApplyToRect(self, target_rect):
        return target_rect.move(self.rect.topleft)

    def change_location_size(self, new_width, new_height):
        self.rect.width = new_width
        self.rect.height = new_height

    def Update(self, target):
        self.rect = self.complex_camera(self.rect, target.rect)

    def complex_camera(self, camera, target_rect):
        width_of_screen = 1280
        half_width_of_screen = width_of_screen / 2
        height_of_screen = 720
        half_height_of_screen = height_of_screen / 2

        l, t, _, _ = target_rect
        _, _, w, h = camera
        l, t, _, _ = -l + half_width_of_screen, -t + half_height_of_screen, w, h

        l = min(0, l)
        l = max(-(camera.width - width_of_screen), l)
        t = max(-(camera.height - height_of_screen), t)
        t = min(0, t)
        return pygame.Rect(l, t, w, h)

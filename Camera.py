import pygame


class Camera(pygame.sprite.Sprite):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.rect = pygame.Rect(0, 0, width, height)

    def Apply(self, target, passed_type="normal"):
        if passed_type == "rect":
            return target.move(self.rect.topleft)
        return target.rect.move(self.rect.topleft)

    def Update(self, target):
        self.rect = self.camera_func(self.rect, target.rect)


def complex_camera(camera, target_rect):
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


camera = Camera(complex_camera, 3000, 32*35)

import pygame


class CollisionObject(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos

# x, y, width, height
ground = CollisionObject(0, 700, 800, 25)
platform1 = CollisionObject(800, 650, 200, 10)
platform2 = CollisionObject(1100, 600, 200, 10)
platform3 = CollisionObject(800, 500, 200, 10)
platform4 = CollisionObject(500, 400, 200, 10)

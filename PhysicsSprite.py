import pygame

class PhysicsSprite(pygame.sprite.Sprite):
    def __init__(self, image, start_x, start_y):
        self.move_x = 0.0
        self.move_y = 0.0
        self.y_velocity = 0.0
        self.downward_acceleration = 0.5

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y

        self.latest_x_direction = ""

    def ApplyCollisions(self, current_location):
        self.rect.x += self.move_x
        collision_list = pygame.sprite.spritecollide(self, current_location.collisions, False)
        for collision_object in collision_list:
            collision_object.HorizontalCollision(self)

        self.rect.y += self.move_y
        collision_list = pygame.sprite.spritecollide(self, current_location.collisions, False)
        for collision_object in collision_list:
            collision_object.VerticalCollision(self)

    def ApplyGravity(self):
        self.y_velocity += self.downward_acceleration
        if self.y_velocity > 10:
            self.y_velocity = 10
        self.move_y += self.y_velocity

    def HitGround(self):
        self.y_velocity = 0.0

    def UpdateXDirection(self, x_direction):
        self.latest_x_direction = x_direction

    def FacingRight(self):
        if self.latest_x_direction == "right":
            return True
        else: return False

    def FacingLeft(self):
        if self.latest_x_direction == "left":
            return True
        else: return False

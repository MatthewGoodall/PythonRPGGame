import pygame
import Player

class CollisionObject(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos

    # No Downward Collision If Down Key Is Pressed
    def CanFallThroughIfDownPressed(self, the_sprite):
        if the_sprite.move_y > 0.0 and not the_sprite.down_pressed:
            if not the_sprite.rect.bottom > self.rect.bottom:
                the_sprite.rect.bottom = self.rect.top
                the_sprite.HitGround()

    # Downward Collision
    def CanNotFallThrough(self, the_sprite):
        if the_sprite.move_y > 0.0:
            the_sprite.rect.bottom = self.rect.top
            the_sprite.HitGround()

    def CanFallThrough(self, the_sprite):
        pass

    # No Upward Collision
    def CanJumpThrough(self, the_sprite):
        pass

    # Upward Collision
    def CanNotJumpThrough(self, the_sprite):
        if the_sprite.move_y < 0.0:
            the_sprite.rect.top = self.rect.bottom

    # No Horizontal Collision
    def CanWalkPast(self, the_sprite):
        pass

    # Horizontal Collision
    def CanNotWalkPast(self, the_sprite):
        if the_sprite.move_x > 0.0:
            the_sprite.rect.right = self.rect.left
        elif the_sprite.move_x < 0.0:
            the_sprite.rect.left = self.rect.right


class SolidObject(CollisionObject):
    def __init__(self, x_pos, y_pos, width, height):
        super().__init__(x_pos, y_pos, width, height)

    def HorizontalCollision(self, the_sprite):
        self.CanNotWalkPast(the_sprite)

    def VerticalCollision(self, the_sprite):
        self.CanNotFallThrough(the_sprite)
        self.CanNotJumpThrough(the_sprite)

class Platform(CollisionObject):
    def __init__(self, x_pos, y_pos, width, height):
        super().__init__(x_pos, y_pos, width, height)

    def HorizontalCollision(self, the_sprite):
        if isinstance(the_sprite, Player.Player):
            self.CanWalkPast(the_sprite)
        else:
            self.CanNotWalkPast(the_sprite)

    def VerticalCollision(self, the_sprite):
        if isinstance(the_sprite, Player.Player):
            self.CanFallThroughIfDownPressed(the_sprite)
            self.CanJumpThrough(the_sprite)
        else:
            self.CanNotFallThrough(the_sprite)
            self.CanNotJumpThrough(the_sprite)


class Ladder(CollisionObject):
    def __init__(self, x_pos, y_pos, width, height):
        super().__init__(x_pos, y_pos, width, height)

    def HorizontalCollision(self, the_sprite):
        self.CanWalkPast(the_sprite)

    def VerticalCollision(self, the_sprite):
        self.CanJumpThrough(the_sprite)

class Gateway(CollisionObject):
    def __init__(self, x_pos, y_pos, width, height, gateway_name, travel_location):
        super().__init__(x_pos, y_pos, width, height)
        self.gateway_name = gateway_name
        self.travel_location = travel_location
        self.location = None

    def HorizontalCollision(self, the_sprite):
        self.CanWalkPast(the_sprite)

    def VerticalCollision(self, the_sprite):
        self.CanJumpThrough(the_sprite)
        self.CanFallThrough(the_sprite)

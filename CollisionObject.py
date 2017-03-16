import pygame


class CollisionObject(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos

    # No Downward Collision If Down Key Is Pressed
    def CanFallThroughIfDownPressed(self, the_player):
        if the_player.move_y > 0.0 and not the_player.down_pressed:
            if not the_player.rect.bottom > self.rect.bottom:
                the_player.rect.bottom = self.rect.top
                the_player.HitGround()

    # Downward Collision
    def CanNotFallThrough(self, the_player):
        if the_player.move_y > 0.0:
            the_player.rect.bottom = self.rect.top
            the_player.can_jump = True
            the_player.HitGround()

    def CanFallThrough(self, the_player):
        pass

    # No Upward Collision
    def CanJumpThrough(self, the_player):
        pass

    # Upward Collision
    def CanNotJumpThrough(self, the_player):
        if the_player.move_y < 0.0:
            the_player.rect.top = self.rect.bottom

    # No Horizontal Collision
    def CanWalkPast(self, the_player):
        pass

    # Horizontal Collision
    def CanNotWalkPast(self, the_player):
        if the_player.move_x > 0.0:
            the_player.rect.right = self.rect.left
        elif the_player.move_x < 0.0:
            the_player.rect.left = self.rect.right


class SolidObject(CollisionObject):
    def __init__(self, x_pos, y_pos, width, height):
        super().__init__(x_pos, y_pos, width, height)

    def HorizontalCollision(self, the_player):
        self.CanNotWalkPast(the_player)

    def VerticalCollision(self, the_player):
        self.CanNotFallThrough(the_player)
        self.CanNotJumpThrough(the_player)

class Platform(CollisionObject):
    def __init__(self, x_pos, y_pos, width, height):
        super().__init__(x_pos, y_pos, width, height)

    def HorizontalCollision(self, the_player):
        self.CanWalkPast(the_player)

    def VerticalCollision(self, the_player):
        self.CanFallThroughIfDownPressed(the_player)
        self.CanJumpThrough(the_player)


class Ladder(CollisionObject):
    def __init__(self, x_pos, y_pos, width, height):
        super().__init__(x_pos, y_pos, width, height)

    def HorizontalCollision(self, the_player):
        self.CanWalkPast(the_player)

    def VerticalCollision(self, the_player):
        self.CanJumpThrough(the_player)

class Gateway(CollisionObject):
    def __init__(self, x_pos, y_pos, width, height, gateway_name, travel_location):
        super().__init__(x_pos, y_pos, width, height)
        self.gateway_name = gateway_name
        self.travel_location = travel_location
        self.location = None

    def HorizontalCollision(self, the_player):
        self.CanWalkPast(the_player)

    def VerticalCollision(self, the_player):
        self.CanJumpThrough(the_player)
        self.CanFallThrough(the_player)

import sys, pygame
import time  # i'm almost out of thyme (Gul'dan)
from Enemy import *  # has been slain
from Player import *
from Animation import *
from Item import *
from CollisionObject import *
from GUI import *
from Camera import *
import pytmx
import TileRender
import math

pygame.init()
pygame.mixer.init()

# Set basic colors
color_black = 0, 0, 0
color_red = 255, 0, 0
color_green = 0, 255, 0
color_sky = 30, 144, 255

# Set screen dimensions
size = width, height = 1280, 720
# Create screen
screen = pygame.display.set_mode(size)
background = pygame.image.load("Resources/SinglePhotos/ForestBackground.png")
# Add sprites to corresponding sprite group-----------------------------
enemy_sprites = pygame.sprite.Group(squid, dragon_hatchling)

player_sprite = pygame.sprite.GroupSingle(player)
platform_objects = pygame.sprite.Group(platform1, platform2, platform3, platform4, ground)
gui_sprites = pygame.sprite.Group(health_bar, mana_bar)
collidables = pygame.sprite.Group(enemy_sprites, platform_objects)
game_objects = pygame.sprite.Group(enemy_sprites, player_sprite, platform_objects)
# Every single sprite
all_sprites = pygame.sprite.Group(enemy_sprites, player_sprite, platform_objects, gui_sprites)
# ------------------------------------------------------------------------
# Background music
backsound_sound = pygame.mixer.music
backsound_sound.load("Resources/Audio/Ambient.mp3")

clock = pygame.time.Clock()

screen_rect = screen.get_rect()

tmx_file = "Resources/TileMaps/Test.tmx"
tile_renderer = TileRender.Renderer(tmx_file)

map_surface = tile_renderer.make_map()
map_rect = map_surface.get_rect()

items = []

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                player.Attack(screen, enemy_sprites)
                print(str(squid.health))

    # Update player movement--------------------------------
    keys = pygame.key.get_pressed()
    player.moving_right = keys[pygame.K_d]
    player.moving_left = keys[pygame.K_a]

    # Check for player attacking
    if keys[pygame.K_SPACE]:
        player.Jump()
    if keys[pygame.K_i]:
        for item in items:
            print(items[items])

    # Checks if living things are alive if not then kill them
    for being in game_objects:
        if not being.alive:
            game_objects.remove(being)
            items.append(enemy.typeOfReward)


    # Update player location and animation------------------
    player.Update(pygame.time.get_ticks(), collidables)

    for enemy in enemy_sprites:
        if enemy.alive:
            enemy.updateAnimation(pygame.time.get_ticks())
            if not abs(player.rect.x - enemy.rect.x) < 200.0:
                enemy.walkPath()
            else:
                enemy.chasePlayer(player_sprite)

    # Clear the screen
    screen.fill(color_sky)
    camera.Update(player)
    screen.blit(map_surface, (0, 0))
    # Draw sprites
    for sprite in game_objects:
        screen.blit(sprite.image, camera.Apply(sprite))
    for sprite in gui_sprites:
        screen.blit(sprite.image, (sprite.rect.x, sprite.rect.y))

    # Update the display
    pygame.display.toggle_fullscreen()
    pygame.display.flip()
    clock.tick(60)

# Now exit the program
pygame.quit()

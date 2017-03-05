import sys, pygame
import time  # i'm almost out of thyme (Gul'dan)
import Enemy  # has been slain
from Player import *
from Camera import *
import Animation
import Item
from CollisionObject import *
import GUI
import pytmx
import TileRender
import math


pygame.init()
pygame.mixer.init()

# Set basic colors
color_black = 0, 0, 0
color_red = 255, 0, 0
color_green = 0, 255, 0
color_blue = 0, 0, 255
color_sky = 30, 144, 255

# Set screen dimensions
size = width, height = 1280, 720
# Create screen
screen = pygame.display.set_mode(size)

# Add sprites to corresponding list-----------------------------
enemy_sprites = [Enemy.squid, Enemy.dragon_hatchling, Enemy.henery]
player_sprite = [player]

gui_sprites = [GUI.health_bar,
               GUI.mana_bar]

game_sprites = enemy_sprites + player_sprite
# Every single sprite
all_sprites = enemy_sprites + gui_sprites + player_sprite
#------------------------------------------------------------------------
# Background music
backsound_sound = pygame.mixer.music
backsound_sound.load("Resources/Audio/Ambient.mp3")

clock = pygame.time.Clock()

screen_rect = screen.get_rect()

tmx_file = "Resources/TileMaps/Test.tmx"
tile_renderer = TileRender.Renderer(tmx_file)

map_surface = tile_renderer.make_map()
map_rect = map_surface.get_rect()

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                player.Attack(screen, enemy_sprites)
            elif event.key == pygame.K_SPACE:
                player.Jump()
            elif event.key == pygame.K_i:
                for item in player.items:
                    print(item)
                print("------")

    # Update player movement--------------------------------
    keys = pygame.key.get_pressed()
    player.jump_pressed = keys[pygame.K_SPACE]
    player.moving_up = keys[pygame.K_w]
    player.moving_right = keys[pygame.K_d]
    player.moving_down = keys[pygame.K_s]
    player.moving_left = keys[pygame.K_a]

    # Checks if living things are alive if not then kill them
    for being in game_sprites:
        if not being.alive:
            game_sprites.remove(being)
            if isinstance(being, Player):
                player_sprite.remove(being)
            else:
                enemy_sprites.remove(being)

    # Update player location and animation------------------
    player.Update(pygame.time.get_ticks(), tile_renderer.ground, tile_renderer.platforms, tile_renderer.ladders)

    for enemy in enemy_sprites:
        if enemy.alive:
            enemy.updateAnimation(pygame.time.get_ticks())
            if not abs(player.rect.centerx - enemy.rect.centerx) < 300.0:
                enemy.walkPath()
            else:
                enemy.chasePlayer(collisions = tile_renderer.ground + tile_renderer.platforms)

    # Clear the screen
    screen.fill(color_sky)
    camera.Update(player)
    screen.blit(map_surface, camera.Apply(map_rect, "rect"))
    # Draw sprites
    for sprite in game_sprites:
        screen.blit(sprite.image, camera.Apply(sprite))
    for sprite in gui_sprites:
        screen.blit(sprite.image, (sprite.rect.x, sprite.rect.y))

    # Update the display
    pygame.display.toggle_fullscreen()
    pygame.display.flip()
    clock.tick(120)

# Now exit the program
pygame.quit()

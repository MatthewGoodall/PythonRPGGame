import pygame, sys 
import time #i'm almost out of thyme (Gul'dan)
from Enemy import * #has been slain
from Player import *
from Animation import *
from Item import *
from CollisionObject import *

pygame.init()
pygame.mixer.init()

# Set basic colors
color_black = 0, 0, 0
color_red = 255,0,0
color_green = 0,255,0
# Set screen dimensions
size = width, height = 1280, 720
# Create screen
screen = pygame.display.set_mode(size)
background = pygame.image.load("Resources/Single photos/forest_background.png")
#Create Sprite groups
all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
player_sprite = pygame.sprite.GroupSingle()
collision_sprites = pygame.sprite.Group()
#Add sprites to corresponding sprite group
all_sprites.add(squid)
all_sprites.add(player)
all_sprites.add(ground)
all_sprites.add(platform)
player_sprite.add(player)
enemy_sprites.add(squid)
collision_sprites.add(ground)
collision_sprites.add(platform)

#Background music starts
backsound_sound = pygame.mixer.music
backsound_sound.load("Resources/Audio/ambientSounds.mp3")
backsound_sound.play()

clock = pygame.time.Clock()

exit = False
while not exit:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      exit = True
      
  # Update player movement--------------------------------
  keys = pygame.key.get_pressed()
  player.movingRight = keys[pygame.K_d]
  player.movingLeft = keys[pygame.K_a]
  player.jumping = keys[pygame.K_SPACE]
  
  # Check for player attacking
  if keys[pygame.K_SPACE]:
    player.Attack(enemy_sprites)
  
  # Update player location and animation------------------
  player.Update(pygame.time.get_ticks(), collision_sprites)

  for enemy in enemy_sprites:
    enemy.updateAnimation(pygame.time.get_ticks())
    squid.chasePlayer(player_sprite)

  #Checks if living things are alive if not then kill them
  for living_being in all_sprites:
    if living_being.alive == False:
      all_sprites.remove(living_being)
    
  # Clear the screen
  screen.fill(color_black)
  
  # Draw background
  screen.blit(background, (0, 0))
	
  # Draw sprites
  all_sprites.draw(screen)
  
  # Update the display
  pygame.display.flip()
  clock.tick(60)
  
# Now exit the program
pygame.quit()

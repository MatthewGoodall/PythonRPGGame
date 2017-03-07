import sys
import pygame
import time  # i'm almost out of thyme (Gul'dan)

import Player
import Enemy  # has been slain
import Animation
import GUI
import TileRender
import Location
import Camera
import NPC
import Item
import CollisionObject
import JSON_Reader

pygame.init()
pygame.mixer.init()
class Game:
    def __init__(self):
        # Set screen dimensions
        self.screen_width = 1280
        self.screen_height = 780
        self.screen_size = self.screen_width, self.screen_height
        self.screen = pygame.display.set_mode(self.screen_size)
        self.player = Player.Player()
        # ms delay defaults to 500ms
        self.player.walking_right_animation = Animation.Animation("Resources/Spritesheets/PlayerWalkingRight.png", 8, 16, 4, 4)
        self.player.walking_right_animation.ms_delay = 125
        self.player.walking_left_animation = Animation.Animation("Resources/Spritesheets/PlayerWalkingLeft.png", 8, 16, 4, 4)
        self.player.walking_left_animation.ms_delay = 125
        self.player.idle_right_animation = Animation.Animation("Resources/Spritesheets/PlayerIdleRight.png", 8, 16, 2, 4)
        self.player.idle_left_animation = Animation.Animation("Resources/Spritesheets/PlayerIdleLeft.png", 8, 16, 2, 4)
        self.player.SetPlayer()
        self.squid_spawning = Animation.Animation("Resources/Spritesheets/Squid.png", 19, 23, 1, 1)
        self.squid_spawning.type = "spawning"
        self.squid_idle = Animation.Animation("Resources/SinglePhotos/Squid.png", 19, 23, 1, 1)

        self.dragon_idle = Animation.Animation("Resources/Spritesheets/DragonLeft.png", 20, 20, 1, 8)
        self.dragon_spawning = Animation.Animation("Resources/Spritesheets/DragonLeft.png", 20, 20, 1, 8)
        self.dragon_spawning.type = "spawning"

        self.hen_idle = Animation.Animation("Resources/Spritesheets/Henrey.png", 18, 18, 1, 1)
        self.hen_spawning = Animation.Animation("Resources/Spritesheets/Henrey.png", 18, 18, 1, 1)
        self.hen_spawning.type = "spawning"

        self.health_bar_anim = Animation.Animation("Resources/Spritesheets/HealthBar.png", 66, 66, 2, 3)
        self.mana_bar_anim = Animation.Animation("Resources/Spritesheets/ManaBar.png", 66, 66, 1, 3)
        # health, damage, numberOfLoot, typeOfReward, spawnPos_X, spawnPos_Y, spawn_animation, walkLoop_start, walkLoop_end
        self.squid = Enemy.Enemy(10, 5, 1, "Sword", 100, 650, self.squid_spawning, 0, 650)
        self.dragon_hatchling = Enemy.Enemy(10, 1, 1, "Gold", 150, 650, self.dragon_spawning, 0, 650)
        self.henery = Enemy.Enemy(10, 5, 1, "Gold", 150, 650, self.hen_spawning, 0, 650)
        self.squid.idle_animation = self.squid_idle
        self.dragon_hatchling.idle_animation = self.dragon_idle
        self.henery.idle_animation = self.hen_idle
        self.camera = Camera.Camera(32*64, 64*64)
        self.clock = pygame.time.Clock()
        self.a_town = Location.Location("Resources/TileMaps/town.tmx")
        self.other_location = Location.Location("Resources/TileMaps/test.tmx")
        self.a_town.CreateMap()
        self.current_location = self.a_town
        self.current_enemies = self.current_location.enemies
        self.GUI = []


    def Setup(self):
        self.camera.Update(self.player)

    def GameLoop(self):
        self.running = True
        while self.running:
            self.HandleEvents()
            self.GetInput()
            self.UpdateSprites()
            self.ClearScreen()
            self.DrawScreen()
            self.DisplayScreen()
            self.HandleFrameRate(120)

    def Quit(self):
        running = False
        pygame.quit()

    def HandleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.player.Attack(self.screen)
                elif event.key == pygame.K_i:
                    for item in self.player.items:
                        print(item)
                    print("------")
                elif event.key == pygame.K_SPACE:
                    self.player.Interact()
                    """
                    text = str(var).strip("[]""'")
                    font = pygame.font.Font(None, 100)
                    text = font.render(text, True, (50, 58, 50))
                    screen.blit(text, [400, 300])
                    """
                elif event.key == pygame.K_ESCAPE:
                    Level.ChangeLevel(Level.level_2)
                    Level.current_level = Level.level_2

    def GetInput(self):
        # Update player movement--------------------------------
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.Jump()
        self.player.right_pressed = keys[pygame.K_d]
        self.player.down_pressed = keys[pygame.K_s]
        self.player.left_pressed = keys[pygame.K_a]

    def UpdateSprites(self):
        self.UpdatePlayer()
        self.UpdateEnemies()

    def UpdatePlayer(self):
        if self.player.alive:
            self.player.UpdateMovement(self.current_location)
            self.player.UpdateAnimation(pygame.time.get_ticks())
        else:
            self.KillPlayer()

    def UpdateEnemies(self):
        for enemy in self.current_enemies:
            if self.enemy.alive:
                enemy.UpdateAnimation(pygame.time.get_ticks())
                if abs(self.player.rect.centerx - enemy.rect.centerx) < 300.0:
                    enemy.ChasePlayer()
                else:
                    enemy.WalkPath()
            else:
                self.KillEnemy()

    def KillPlayer(self):
        #Game over(TO BE IMPLEMENTED)
        pass

    def KillEnemy(self, enemy_to_kill):
        current_enemies.remove(enemy_to_kill)

    def ClearScreen(self):
        color_of_sky = 30, 144, 255
        self.screen.fill(color_of_sky)

    def DrawScreen(self):
        self.camera.Update(self.player)
        self.current_location.Render(self.screen)

        self.screen.blit(self.player.image, self.camera.ApplyToSprite(self.player))

        for enemy in self.current_enemies:
            self.screen.blit(enemy.image, self.camera.ApplyToSprite(enemy))

        for gui_element in self.GUI:
            self.screen.blit(gui_element.image, (gui_element.x, gui_element.y))

    def DisplayScreen(self):
        pygame.display.flip()

    def HandleFrameRate(self, frames_per_second):
        self.clock.tick(frames_per_second)

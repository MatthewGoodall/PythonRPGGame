import sys
import pygame
import time  # i'm almost out of thyme (Gul'dan)

import Player
import Enemy  # has been slain
import Animation
import GUI
import TileRender
import Level
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
        self.screen_size = self.screen_width, self.screen_size
        self.screen = pygame.display.set_mode(size)

        self.camera = Camera.Camera()
        self.clock = pygame.time.Clock()
        self.a_town = Level.Level("Resources/TileMaps/town.tmx")
        self.other_location = Level.Level("Resources/TileMaps/test.tmx")
        self.current_level = a_town
        self.player = Player.Player()

    def Setup(self):
        pass

    def GameLoop(self):
        running = True
        while running:
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
                done = True
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
            self.player.UpdateMovement
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
        screen.fill(color_of_sky)

    def DrawScreen(self):
        self.screen.blit(self.player.image, self.camera.ApplyToSprite(self.player))

        for enemy in self.current_enemies:
            self.screen.blit(enemy.image, self.camera.ApplyToSprite(enemy))

        for gui_element in self.GUI:
            self.screen.blit(gui_element.image, (gui_element.x, gui_element.y))

    def DisplayScreen(self):
        pygame.display.flip()

    def HandleFrameRate(self, frames_per_second):
        self.clock.tick(frames_per_second)

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
        self.locations = []
        self.current_location = None
        self.GUI = []
        self.camera = Camera.Camera(32*32, 32*48)
        self.player = Player.Player()

    def Setup(self):
        self.player.Load()

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
                if event.key == pygame.K_q:
                    self.player.Attack(self.current_location)
                elif event.key == pygame.K_i:
                    for item in self.player.items:
                        print(item)
                    print("------")
                elif event.key == pygame.K_e:
                    self.player.Interact()
                    """
                    text = str(var).strip("[]""'")
                    font = pygame.font.Font(None, 100)
                    text = font.render(text, True, (50, 58, 50))
                    screen.blit(text, [400, 300])
                    """
                elif event.key == pygame.K_ESCAPE:
                    Level.ChangeLevel(Level.level_2)
                    Level.current_location = Level.level_2

    def GetInput(self):
        # Update player movement--------------------------------
        keys = pygame.key.get_pressed()
        self.player.up_pressed = keys[pygame.K_w]
        self.player.right_pressed = keys[pygame.K_d]
        self.player.down_pressed = keys[pygame.K_s]
        self.player.left_pressed = keys[pygame.K_a]
        self.player.jump_pressed = keys[pygame.K_SPACE]
        if self.player.jump_pressed:
            self.player.Jump()

    def UpdateSprites(self):
        self.UpdatePlayer()
        self.UpdateEnemies()
        self.UpdateGUI()

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

    def UpdateGUI(self):
        for gui_element in self.GUI:
            gui_element.UpdateAnimation()

    def KillPlayer(self):
        # Game over(TO BE IMPLEMENTED)
        pass

    def KillEnemy(self, enemy_to_kill):
        self.current_location.current_enemies.remove(enemy_to_kill)

    def ClearScreen(self):
        color_of_sky = 30, 144, 255
        self.screen.fill(color_of_sky)

    def DrawScreen(self):
        self.camera.Update(self.player)
        self.screen.blit(self.current_location.map_surface, self.camera.ApplyToRect(self.current_location.map_rect))

        self.screen.blit(self.player.image, self.camera.ApplyToSprite(self.player))

        for enemy in self.current_enemies:
            self.screen.blit(enemy.image, self.camera.ApplyToSprite(enemy))

        for gui_element in self.GUI:
            self.screen.blit(gui_element.image, (gui_element.x, gui_element.y))

    def DisplayScreen(self):
        pygame.display.flip()

    def HandleFrameRate(self, frames_per_second):
        self.clock.tick(frames_per_second)

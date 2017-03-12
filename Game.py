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
import JSONDataReader

pygame.init()
pygame.mixer.init()
class Game:
    def __init__(self):
        # Set screen dimensions
        self.screen_width = 1280
        self.screen_height = 780
        self.screen_size = self.screen_width, self.screen_height
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()

        self.json_reader = JSONDataReader.JSONDataReader()
        self.json_reader.MakeAnimations("Resources/JSON Data/ANIMATION_DATA.json")
        self.json_reader.MakeEnemies("Resources/JSON Data/ENEMY_DATA.json")
        self.json_reader.MakeNPCs("Resources/JSON Data/NPC_DATA.json")
        self.json_reader.MakeLocations("Resources/JSON Data/LOCATION_DATA.json")
        self.json_reader.PopulateLocations()

        self.locations = self.json_reader.locations
        self.current_location = self.json_reader.GetLocation("town")
        self.enemies = list(self.current_location.enemies)
        self.NPCs = self.current_location.NPCs
        self.GUI = GUI.GUI(self.json_reader)
        self.camera = Camera.Camera(32*64, 32*48, self.screen_width, self.screen_height)
        self.player = Player.Player(self.json_reader)

    def StartScreen(self):
        self.running = True
        start_screen_image = pygame.image.load("Resources/SinglePhotos/StartMenu.png")
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.running = False
            self.screen.fill((0, 0, 0))
            self.screen.blit(start_screen_image, (0, 0))
            pygame.display.flip()

    def Setup(self):
        pass

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
                    self.player.Attack(self.enemies)
                elif event.key == pygame.K_i:
                    for item in self.player.items:
                        print(item)
                    print("------")
                elif event.key == pygame.K_e:
                    self.PlayerInteract()
                    """
                    text = str(var).strip("[]""'")
                    font = pygame.font.Font(None, 100)
                    text = font.render(text, True, (50, 58, 50))
                    screen.blit(text, [400, 300])
                    """
                elif event.key == pygame.K_h:
                    self.player.current_health -= 1
                elif event.key == pygame.K_ESCAPE:
                    pass

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

    def PlayerInteract(self):
        self.player.NPCCollision(self.current_location)
        gateway = self.player.GatewayCollision(self.current_location)
        if gateway:
            self.ChangeLocation(gateway)

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
        for enemy in self.enemies:
            if enemy.alive:
                enemy.UpdateAnimation(pygame.time.get_ticks())
                if abs(self.player.rect.centerx - enemy.rect.centerx) < 300.0:
                    enemy.ChasePlayer(self.current_location.collisions, self.player)
                else:
                    enemy.WalkPath()
            else:
                self.KillEnemy(enemy)

    def UpdateGUI(self):
        self.GUI.Update(self.player)

    def KillPlayer(self):
        # Game over(TO BE IMPLEMENTED)
        pass

    def KillEnemy(self, enemy_to_kill):
        self.enemies.remove(enemy_to_kill)

    def ClearScreen(self):
        color_of_sky = 30, 144, 255
        self.screen.fill(color_of_sky)

    def DrawScreen(self):
        self.camera.Update(self.player)
        self.screen.blit(self.current_location.map_surface, self.camera.ApplyToRect(self.current_location.map_rect))

        self.screen.blit(self.player.image, self.camera.ApplyToSprite(self.player))

        for enemy in self.enemies:
            self.screen.blit(enemy.image, self.camera.ApplyToSprite(enemy))

        for npc in self.NPCs:
            self.screen.blit(npc.image, self.camera.ApplyToSprite(npc))

        for gui_element in self.GUI.gui_items:
            self.screen.blit(gui_element.image, (gui_element.rect.x, gui_element.rect.y))

    def DisplayScreen(self):
        pygame.display.flip()

    def HandleFrameRate(self, frames_per_second):
        self.clock.tick(frames_per_second)

    def ChangeLocation(self, gateway):
        for a_gateway in TileRender.Renderer.all_gateways:
            if a_gateway.gateway_name == gateway.travel_location:
                gateway_travelling_to = a_gateway

        self.player.rect.x = gateway_travelling_to.rect.x
        self.player.rect.y = gateway_travelling_to.rect.y
        self.current_location = self.json_reader.GetLocation(gateway_travelling_to.location.name)
        self.enemies = list(self.current_location.enemies)
        for enemy in self.enemies:
            enemy.Respawn()
        self.NPCs = self.current_location.NPCs
        self.camera.ChangeLocationSize(self.current_location.map_rect.width, self.current_location.map_rect.height)

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
import random
pygame.init()
pygame.mixer.init()
class Game:
    def __init__(self):
        # Set Screen Dimensions
        self.screen_width = 1024
        self.screen_height = 576
        self.screen_size = self.screen_width, self.screen_height
        # Create Screen
        self.display_info = pygame.display.Info()
        self.draw_screen = pygame.display.set_mode((self.display_info.current_w, self.display_info.current_h), pygame.FULLSCREEN)
        self.screen = pygame.Surface((self.screen_width, self.screen_height))
        # Create Clock
        self.clock = pygame.time.Clock()

        # Read and Gather JSON Data
        self.json_reader = JSONDataReader.JSONDataReader()
        self.json_reader.MakeAnimations("Resources/JSON Data/ANIMATION_DATA.json")
        self.json_reader.MakeEnemies("Resources/JSON Data/ENEMY_DATA.json")
        self.json_reader.MakeNPCs("Resources/JSON Data/NPC_DATA.json")
        self.json_reader.MakeLocations("Resources/JSON Data/LOCATION_DATA.json")
        self.json_reader.MakePotion("resources/JSON Data/POTION_DATA.json")
        self.json_reader.MakeWeapon("Resources/JSON Data/ITEM_DATA.json")
        self.json_reader.PopulateLocations()


        # Set current location of the player
        self.current_location = self.json_reader.GetLocation("town")
        # Seperate enemies from the location, so they will "respawn" when you enter the location
        self.current_enemies = list(self.current_location.enemies)

        # Create GUI, Camera that follows the player, and the player itself
        self.GUI = GUI.GUI(self.json_reader)
        self.camera = Camera.Camera(self.current_location.map_rect.width, self.current_location.map_rect.height, self.screen_width, self.screen_height)
        self.player = Player.Player(self.json_reader)

        # Set flags
        self.game_running = True
        self.paused = False

    def StartScreen(self):
        start_screen_image = pygame.image.load("Resources/SinglePhotos/StartMenu.png")
        start_screen = True
        while start_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_running = False
                elif event.type == pygame.KEYDOWN:
                    start_screen = False
            self.ClearScreen()
            self.screen.blit(start_screen_image, (0, 0))
            self.DisplayScreen()

    def Setup(self):
        pass

    def GameLoop(self):
        while self.game_running:
            if not self.paused:
                self.HandleEvents()
                self.GetInput()
                self.UpdateSprites()
            else:
                self.HandleMainEvents()

            self.ClearScreen()
            self.DrawGameScreen()
            if self.paused:
                self.DrawPausedScreen()

            self.DisplayScreen()
            self.HandleFrameRate(60)

    def Quit(self):
        pygame.quit()

    def HandleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.player.Attack(self.current_enemies)

                elif event.key == pygame.K_i:
                    self.player.inventory.PrintInventory()

                elif event.key == pygame.K_e:
                    self.PlayerInteract()

                elif event.key == pygame.K_ESCAPE:
                    if self.paused:
                        self.paused = False
                    elif not self.paused:
                        self.paused = True

                elif event.key == pygame.K_F1:
                    self.game_running = False

    def HandleMainEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.paused:
                        self.paused = False
                    elif not self.paused:
                        self.paused = True
                elif event.key == pygame.K_F1:
                    self.game_running = False

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
        if self.player.npc_talking_to:
            if self.GUI.message_box_shown:
                self.GUI.RemoveMessageBox()
            else:
                self.GUI.MakeMessageBox(self.player.npc_talking_to.dialogue, self.player.npc_talking_to.close_up)

        self.player.ItemDropCollision(self.current_location)
        gateway = self.player.GatewayCollision(self.current_location)
        if gateway:
            self.ChangeLocation(gateway)

    def UpdateSprites(self):
        self.UpdatePlayer()
        self.UpdateEnemies()
        self.UpdateGUI()
        self.UpdateItemDrops()

    def UpdatePlayer(self):
        if self.player.alive:
            self.player.UpdateMovement(self.current_location)
            self.player.UpdateAnimation(pygame.time.get_ticks())
        else:
            self.KillPlayer()

    def UpdateEnemies(self):
        for enemy in self.current_enemies:
            if enemy.alive:
                enemy.UpdateAnimation(pygame.time.get_ticks())
                if abs(self.player.rect.centerx - enemy.rect.centerx) < 300.0:
                    enemy.ChasePlayer(self.current_location.collisions, self.player)
                else:
                    enemy.WalkPath()
            else:
                self.KillEnemy(enemy)

        for location in self.json_reader.locations:
            for enemy in location.enemies:
                if enemy not in self.current_enemies:
                    enemy.WalkPath()

    def UpdateGUI(self):
        self.GUI.Update(self.player)

    def UpdateItemDrops(self):
        for item_drop in self.current_location.item_drops:
            item_drop.Update(self.current_location.collisions)

    def KillPlayer(self):
        # Game over(TO BE IMPLEMENTED)
        pass

    def KillEnemy(self, enemy_to_kill):
        item = Item.ItemDrop(enemy.RandomGoldDrop, enemy_to_kill.rect.x, enemy_to_kill.rect.y)
        self.current_location.item_drops.append(item)
        self.current_enemies.remove(enemy_to_kill)

    def ClearScreen(self):
        color_of_sky = 30, 144, 255
        self.screen.fill(color_of_sky)

    def DrawGameScreen(self):
        self.camera.Update(self.player)
        self.screen.blit(self.current_location.map_surface, self.camera.ApplyToRect(self.current_location.map_rect))

        self.screen.blit(self.player.image, self.camera.ApplyToSprite(self.player))

        for enemy in self.current_enemies:
            self.screen.blit(enemy.image, self.camera.ApplyToSprite(enemy))

        for npc in self.current_location.NPCs:
            self.screen.blit(npc.image, self.camera.ApplyToSprite(npc))

        for gui_element in self.GUI.gui_items:
            self.screen.blit(gui_element.image, (gui_element.rect.x, gui_element.rect.y))

        for item_drop in self.current_location.item_drops:
            self.screen.blit(item_drop.image, self.camera.ApplyToSprite(item_drop))

    def DrawPausedScreen(self):
        self.screen.blit(self.GUI.pause_screen.image, (self.GUI.pause_screen.rect.x, self.GUI.pause_screen.rect.y))

    def DisplayScreen(self):
        scaled_display = pygame.transform.scale(self.screen, (self.display_info.current_w, self.display_info.current_h), self.draw_screen)
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
        self.current_enemies = list(self.current_location.enemies)
        for enemy in self.current_enemies:
            if not enemy.alive:
                enemy.Respawn()
        self.camera.ChangeLocationSize(self.current_location.map_rect.width, self.current_location.map_rect.height)

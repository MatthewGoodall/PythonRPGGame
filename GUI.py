"""
/ Create GUI bars for things like a health bar or something
/ A gui image for something like a background image that doesnt actually do anything when pressed/hover_image
/ GUI buttons change image to next animation frame when Hovered
/   and you can implement them doing different things when Pressed()
/ make sure to add elements to their respective list
/   (pause or normal hud elements)
/ The resource for creating message boxes are just storing images so they can be passed by reference
/ Messageboxes are made in the game file when the player interacts
/ Every time the gui updates it checks to see if the player is still talking to an NPC
/   if they aren't, remove the current message box being shown
/ Instead of treating each gui element differently in the update function, subclasses are made
/   which do all the work on their side (health bar class grabs the player health from the game class)
"""
import pygame
import Animation
import JSONDataReader
import Messagebox

class GUI:
    def __init__(self, game):
        # Normal game overlay
        self.health_bar = HealthBar(game)
        self.mana_bar = ManaBar(game)
        self.hud_elements = [self.health_bar, self.mana_bar]

        # Pause menu
        self.pause_menu_background = GUIImage("Resources/SinglePhotos/PauseMenuBackground.png", 0, 0)
        self.pause_menu_background.XCenter(game.screen_width)
        self.pause_menu_background.YCenter(game.screen_height)
        self.continue_button = ContinueButton(game)
        self.settings_button = SettingsButton(game)
        self.exit_button = ExitButton(game)
        self.pause_menu_elements = [self.pause_menu_background, self.continue_button, self.settings_button,self.exit_button]
        # Resources for creating message boxes
        self.font = pygame.font.Font("Resources/Fonts/Ringbearer.ttf", 30)
        self.dialogue_frame_image = pygame.image.load("Resources/SinglePhotos/MessageBoxFrame.png")
        self.message_box_shown = False

    def Update(self, game):
        for gui_element in self.hud_elements:
            gui_element.Update(game)

        if game.paused:
            for gui_element in self.pause_menu_elements:
                gui_element.Update(game)

        self.UpdateMessageBox(game)

    def MousePress(self, game):
        for gui_element in self.hud_elements:
            if isinstance(gui_element, GUIButton):
                if gui_element.hovered:
                    gui_element.Pressed(game)

        if game.paused:
            for gui_element in self.pause_menu_elements:
                if isinstance(gui_element, GUIButton):
                    if gui_element.hovered:
                        gui_element.Pressed(game)

    def UpdateMessageBox(self, game):
        if game.player.npc_talking_to == None:
            self.RemoveMessageBox()

    def MakeMessageBox(self, npc):
        message_box = Messagebox.MessageBox(self.dialogue_frame_image, self.font, npc)
        self.hud_elements.append(message_box)
        self.message_box_shown = True

    def RemoveMessageBox(self):
        for gui_element in self.hud_elements:
            if isinstance(gui_element, Messagebox.MessageBox):
                self.hud_elements.remove(gui_element)
                self.message_box_shown = False


class GUIElement(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def XCenter(self, screen_width, offset=0):
        self.rect.x = screen_width / 2 - self.rect.width / 2
        self.rect.x += offset

    def YCenter(self, screen_height, offset=0):
        self.rect.y = screen_height / 2 - self.rect.height / 2
        self.rect.y += offset

    def Update(self, game):
        pass

class GUIImage(GUIElement):
    def __init__(self, image_path, x, y):
        image = pygame.image.load(image_path).convert_alpha()
        super().__init__(image, x, y)

class GUIButton(GUIElement):
    def __init__(self, animation, x, y):
        super().__init__(animation.GetFrame(0), x, y)
        self.normal_image = animation.GetFrame(0)
        self.hover_image = animation.GetFrame(1)

    def Update(self, game):
        self.CheckForHover(game)

        if self.hovered:
            self.Hovered()
        elif not self.hovered:
            self.NotHovered()

    def CheckForHover(self, game):
        self.hovered = self.rect.collidepoint(game.mouse_pos)

    def Hovered(self):
        if self.image is not self.hover_image:
            self.image = self.hover_image

    def NotHovered(self):
        if self.image is not self.normal_image:
            self.image = self.normal_image

    def Pressed(self, game):
        pass

class ContinueButton(GUIButton):
    def __init__(self, game):
        super().__init__(game.json_reader.GetAnimation("continue_option"), 0, 0)
        self.XCenter(game.screen_width)
        self.YCenter(game.screen_height, offset=-30)

    def Pressed(self, game):
        game.paused = False

class SettingsButton(GUIButton):
    def __init__(self, game):
        super().__init__(game.json_reader.GetAnimation("settings_option"), 0, 0)
        self.XCenter(game.screen_width)
        self.YCenter(game.screen_height)

    def Pressed(self, game):
        # Not implemented, will open settings menu
        pass

class ExitButton(GUIButton):
    def __init__(self, game):
        super().__init__(game.json_reader.GetAnimation("quit_option"), 0, 0)
        self.XCenter(game.screen_width)
        self.YCenter(game.screen_height, offset=30)

    def Pressed(self, game):
        game.game_running = False

class GUIBar(GUIElement):
    def __init__(self, animation, x, y):
        super().__init__(animation.GetFirstFrame(), x ,y)
        self.animation = animation

    def Update():
        pass

    def UpdatePercentage(self, current_value, max_value):
        percent_full = (current_value / max_value) * 100
        i = 100
        checking = True
        while checking:
            if percent_full >= i:
                self.image = self.animation.GetFrame(int(i/10))
                checking = False
            i -= 10
            if i < 0:
                checking = False

class HealthBar(GUIBar):
    def __init__(self, game):
        super().__init__(game.json_reader.GetAnimation("health_bar"), 0, 0)

    def Update(self, game):
        self.UpdatePercentage(game.player.current_health, game.player.maximum_health)

class ManaBar(GUIBar):
    def __init__(self, game):
        super().__init__(game.json_reader.GetAnimation("mana_bar"), 126, 0)

    def Update(self, game):
        self.UpdatePercentage(game.player.current_mana, game.player.maximum_mana)

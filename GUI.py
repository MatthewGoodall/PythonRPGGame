import pygame
import Animation
import JSONDataReader
import Messagebox

class GUI:
    def __init__(self, game, json_data):
        # Normal game overlay
        self.health_bar = GUIBar(json_data.GetAnimation("health_bar"), 0, 0)
        self.mana_bar = GUIBar(json_data.GetAnimation("mana_bar"), 126, 0)
        self.hud_elements = [self.health_bar, self.mana_bar]

        # Pause menu
        self.pause_menu_background = GUI_Image("Resources/SinglePhotos/PauseMenuBackground.png", 0, 0)
        self.pause_menu_background.XCenter(game.screen_width)
        self.pause_menu_background.YCenter(game.screen_width)
        self.pause_settings_option = GUI_Button(json_data.GetAnimation("settings_option"), 0, 0)
        self.pause_settings_option.XCenter(game.screen_width)
        self.pause_settings_option.YCenter(game.screen_height)
        self.pause_menu_elements = [self.pause_menu_background, self.pause_settings_option]

        # Resources for creating message boxes
        self.dialogue_frame_image = pygame.image.load("Resources/SinglePhotos/MessageBoxFrame.png")
        self.letters = Messagebox.Letters()
        self.message_box_shown = False

    def Update(self, game):
        self.health_bar.Update(game.player.current_health, game.player.maximum_health)
        self.mana_bar.Update(game.player.current_mana, game.player.maximum_mana)
        if game.player.npc_talking_to == None:
            self.RemoveMessageBox()

        self.pause_settings_option.Update(game.mouse_pos)
        self.pause_menu_background.Update()

    def MakeMessageBox(self, string, picture):
        message_box = Messagebox.MessageBox(self.letters, self.dialogue_frame_image, picture, string)
        self.hud_elements.append(message_box)
        self.message_box_shown = True

    def RemoveMessageBox(self):
        for gui_element in self.hud_elements:
            if isinstance(gui_element, Messagebox.MessageBox):
                self.hud_elements.remove(gui_element)
                self.message_box_shown = False


class GUI_Item(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def XCenter(self, screen_width):
        self.rect.x = screen_width / 2 - self.rect.width / 2

    def YCenter(self, screen_height):
        self.rect.y = screen_height / 2 - self.rect.height / 2

    def Update(self):
        pass

class GUI_Image(GUI_Item):
    def __init__(self, image_path, x, y):
        image = pygame.image.load(image_path).convert_alpha()
        super().__init__(image, x, y)

class GUI_Button(GUI_Item):
    def __init__(self, animation, x, y):
        super().__init__(animation.GetFrame(0), x, y)
        self.normal_image = animation.GetFrame(0)
        self.hover_image = animation.GetFrame(1)

    def Update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.Hovered()
        else:
            self.NotHovered()

    def Hovered(self):
        if self.image is not self.hover_image:
            self.image = self.hover_image

    def NotHovered(self):
        if self.image is not self.normal_image:
            self.image = self.normal_image

class GUIBar(GUI_Item):
    def __init__(self, animation, x, y):
        super().__init__(animation.GetFirstFrame(), x ,y)
        self.animation = animation

    def Update(self, current_value, maximum_value):
        pass
        """
        percent_full = (current_value / maximum_value) * 100
        i = 100
        checking = True
        while checking:
            if percent_full >= i:
                self.image = self.animation.GetFrame(int(i/10))
                checking = False
            i -= 10
            if i < 0:
                checking = False
        """

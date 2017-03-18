import pygame
import Animation
import JSONDataReader
import Messagebox

class GUI:
    def __init__(self, json_data, screen_size):
        self.screen_width = screen_size[0]
        self.screen_height = screen_size[1]
        self.half_screen_width = self.screen_width / 2
        self.half_screen_height = self.screen_height / 2

        self.gui_items = []
        self.health_bar = GUIBar(json_data.GetAnimation("health_bar"), 0, 0)
        self.mana_bar = GUIBar(json_data.GetAnimation("mana_bar"), 126, 0)
        self.gui_items.extend((self.health_bar, self.mana_bar))

        self.pause_gui_items = []
        self.settings_option = Button(json_data.GetAnimation("settings_option"),
                                      self.half_screen_width, self.half_screen_height, True)
        self.pause_gui_items.append(self.settings_option)

        self.message_box_shown = False
        self.dialogue_frame_image = pygame.image.load("Resources/SinglePhotos/MessageBoxFrame.png").convert_alpha()
        self.letters = Messagebox.Letters()

    def Update(self, player, mouse_pos):
        self.health_bar.Update(player.current_health, player.maximum_health)
        self.mana_bar.Update(player.current_mana, player.maximum_mana)
        if player.npc_talking_to == None:
            self.RemoveMessageBox()
        for pause_item in self.pause_gui_items:
            pause_item.Update(mouse_pos)

    def MakeMessageBox(self, string, picture):
        message_box = Messagebox.MessageBox(self.letters, self.dialogue_frame_image, picture, string)
        self.gui_items.append(message_box)
        self.message_box_shown = True

    def RemoveMessageBox(self):
        for gui_item in self.gui_items:
            if isinstance(gui_item, Messagebox.MessageBox):
                self.gui_items.remove(gui_item)
                self.message_box_shown = False

class GUI_Item(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def Update(self):
        pass

class Button(GUI_Item):
    def __init__(self, animation, x, y, is_centered = False):
        super().__init__(animation.GetFrame(0), x, y)
        if is_centered:
            self.rect.x -= self.rect.width / 2

        self.normal_image = animation.GetFrame(0)
        self.hover_image = animation.GetFrame(1)

    def Update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.Hover()
        else:
            self.NotHovered()

    def Hover(self):
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

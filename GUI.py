import pygame
import Animation
import JSONDataReader
import Messagebox

class GUI:
    def __init__(self, json_data):
        self.gui_items = []
        self.health_bar = GUIBar(json_data.GetAnimation("health_bar"), 0, 0)
        self.mana_bar = GUIBar(json_data.GetAnimation("mana_bar"), 126, 0)
        self.gui_items.extend((self.health_bar, self.mana_bar))

        self.pause_screen_image = pygame.image.load("Resources/SinglePhotos/PauseMenu.png")
        self.pause_screen = GUI_Item(self.pause_screen_image, 0, 0)
        self.pause_screen.rect.x = 1024/2 - self.pause_screen.rect.width/2
        self.pause_screen.rect.y = 576/2 - self.pause_screen.rect.height/2
        self.message_box_shown = False
        self.dialogue_frame_image = pygame.image.load("Resources/SinglePhotos/MessageBoxFrame.png").convert_alpha()
        self.letters = Messagebox.Letters()

    def Update(self, player):
        self.health_bar.Update(player.current_health, player.maximum_health)
        self.mana_bar.Update(player.current_mana, player.maximum_mana)
        if player.npc_talking_to == None:
            self.RemoveMessageBox()

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

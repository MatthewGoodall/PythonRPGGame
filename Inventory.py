import pygame
import GUI

class Inventory:
    def __init__(self):
        self.items = []
        self.max_items = 36
        self.gold = 0

    def PrintInventory(self):
        for item in self.items:
            print(item.name)
        print(str(self.gold))
        print("-----------")

    def AddItem(self, item):
        if len(self.items) >= self.max_items:
            print("Can not add item, full inventory")
        else:
            self.items.append(item)

    def AddGold(self, amount):
        self.gold += amount

    def RemoveItem(self, item):
        if item in self.items:
            self.items.remove(item)

    def CanPayGold(self, amount):
        if self.gold - amount < 0:
            print("can not afford")
            return False
        else:
            return True

    def DecreaseGold(self, amount):
        self.gold -= amount

class InventoryGUI(GUI.GUIElement):
    def __init__(self, game):
        self.background = pygame.image.load("Resources/SinglePhotos/InventoryMenuBackground.png").convert_alpha()
        super().__init__(self.background, 0, 0)
        self.inventory_slot = game.json_reader.GetAnimation("inventory_slot")
        self.image = pygame.Surface((self.background.get_width(), self.background.get_height()))
        self.XCenter(game.screen_width)
        self.YCenter(game.screen_height)

    def Update(self, game):
        pass
        """
        inventory = list(game.player.inventory.items)
        for item, slot in zip(inventory, game.player.inventory.max_items):
            print("item name" + item.name)
            print("number:" + str(slot))
        """

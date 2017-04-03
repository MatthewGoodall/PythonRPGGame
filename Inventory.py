import pygame
import GUI
import copy

class Inventory:
    def __init__(self):
        self.item_stacks = []
        self.max_items = 40
        self.gold = 0

    def AddItem(self, item):
        for item_stack in self.item_stacks:
            if item_stack.item_name == item.name:
                item_stack.quantity += 1
                break
        else:
            new_item_stack = ItemStack(item)
            new_item_stack.quantity = 1
            self.item_stacks.append(new_item_stack)


    def AddGold(self, amount):
        self.gold += amount

    def RemoveItem(self, item):
        for item_stack in self.item_stacks:
            if item_stack.item_name == item.name:
                item_stack.quantity -= 1
                if item_stack.quantity <= 0:
                    self.items_stacks.remove(item_stack)
                break
        else:
            print("no item in inventory has been found")

    def CanPayGold(self, amount):
        if self.gold - amount < 0:
            print("can not afford")
            return False
        else:
            return True

    def DecreaseGold(self, amount):
        self.gold -= amount

class ItemStack:
    def __init__(self, item):
        self.item_name = item.name
        self.image = item.image
        self.quantity = 0

class InventoryGUI(GUI.GUIElement):
    def __init__(self, game):
        self.background = pygame.image.load("Resources/SinglePhotos/InventoryMenuBackground.png").convert_alpha()
        super().__init__(self.background, 0, 0)
        self.inventory_slot = game.json_reader.GetAnimation("inventory_slot")
        self.image = pygame.Surface((self.background.get_width(), self.background.get_height()))
        self.XCenter(game.screen_width)
        self.YCenter(game.screen_height)
        self.font = pygame.font.Font("Resources/Fonts/Roboto.ttf", 18)

    def Update(self, game):
        new_image = copy.copy(self.background)
        x = 8
        y = 38
        gap = 8
        for item_stack in game.player.inventory.item_stacks:
            scaled_item_image = pygame.transform.scale(item_stack.image, (64, 64))
            new_image.blit(scaled_item_image, (x, y))

            quantity_of_items = self.font.render(str(item_stack.quantity), 1, (0, 0, 0))
            new_image.blit(quantity_of_items, (x, y))

            x += 64 + gap
            if x >= 10*64 + 10*gap:
                x = 8
                y += 64 + gap

        amount_of_gold = self.font.render(str(game.player.inventory.gold), 1, (0, 0, 0))
        new_image.blit(amount_of_gold, (272*2, 6))

        self.image = new_image

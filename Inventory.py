class Inventory:
    def __init__(self):
        self.items = []
        self.max_items = 30
        self.gold = 0

    def PrintInventory(self):
        for item in self.items:
            print(item.name)
        print("-----------")
        
    def AddItem(self, item):
        if len(self.items) >= 30:
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

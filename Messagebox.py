import pygame

class Letters:
    def __init__(self):
        self.letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k",
                        "l", "m", "n", "o", "p"," q", "r", "s", "t", "u",
                        "v", "w", "x", "y", "z", " "]
        self.alphabet_image = pygame.image.load("Resources/SinglePhotos/Alphabet.png")
        self.letter_dict = {}
        self.letter_images = []
        for x in range(len(self.letters)):
            single_letter = self.alphabet_image.subsurface((x*15,0, 15, 21))
            self.letter_images.append(single_letter)

        for i in range(len(self.letter_images)):
            self.letter_dict[self.letters[i]] = self.letter_images[i]

class MessageBox(pygame.sprite.Sprite):
    def __init__(self, letters, string):
        super().__init__()

        self.image = pygame.Surface((1024, 100))
        self.image.fill((255, 255, 255))
        height = 5
        for char in range(len(string)):
            letter_image = letters.letter_dict[string[char]]
            if char * 20 > 1024:
                height = 50
                width = char - 51
            else:
                width = char
            self.image.blit(letter_image, (width * 20 + 5, height))

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 500

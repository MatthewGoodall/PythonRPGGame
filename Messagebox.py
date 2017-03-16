import pygame
import copy
class Letters:
    def __init__(self):
        self.letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k",
                        "l", "m", "n", "o", "p"," q", "r", "s", "t", "u",
                        "v", "w", "x", "y", "z", " "]
        self.alphabet_image = pygame.image.load("Resources/SinglePhotos/Alphabet.png")
        self.letter_dict = {}
        self.letter_images = []
        length_of_surface = self.alphabet_image.get_width()
        height_of_surface = self.alphabet_image.get_height()
        width_of_one_letter = length_of_surface / len(self.letters)
        for x in range(len(self.letters)):
            single_letter = self.alphabet_image.subsurface((x*width_of_one_letter,0, width_of_one_letter, height_of_surface))
            self.letter_images.append(single_letter)

        for i in range(len(self.letter_images)):
            self.letter_dict[self.letters[i]] = self.letter_images[i]

class MessageBox(pygame.sprite.Sprite):
    def __init__(self, letters, frame_image, npc_picture, string):
        super().__init__()

        self.image = copy.copy(frame_image)
        self.dialogue_box = pygame.Surface((808, 100), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 385
        current_x = 0
        current_y = 0
        letter_width = letters.letter_images[0].get_width()
        letter_height = letters.letter_images[0].get_height()
        spacing = 3
        for char in range(len(string)):
            letter_image = letters.letter_dict[string[char]]
            self.dialogue_box.blit(letter_image, (current_x, current_y))
            current_x += letter_width + spacing
            if current_x + letter_width + spacing > self.rect.width:
                current_x = 0
                current_y += letter_height + 3
        self.image.blit(self.dialogue_box, (204, 12))
        self.image.blit(npc_picture, (12, 12))

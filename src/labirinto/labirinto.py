import pygame
import random

class Parede(pygame.sprite.Sprite):
    def __init__(self, x, y, lista_telhados):
        super().__init__()
        self.image = random.choice(lista_telhados)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

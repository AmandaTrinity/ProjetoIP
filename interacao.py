# uma nova classe precisa ser criada
# COORDENADAS (x, y) que o jogador será capaz de interagir

import pygame
from config import *

class PontoDeInteresse(pygame.sprite.Sprite):
       
       def __init__(self, x, y):
        super().__init__()

        # enquanto nao tem cenário
        self.image = pygame.Surface((70, 100)) # retângulo maior
        self.image.fill(cinza)
        self.rect = self.image.get_rect()
        
        # a posicao dele no mapa com base nos argumentos x e y
        self.rect.topleft = (x, y)
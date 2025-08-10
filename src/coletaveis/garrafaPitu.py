import pygame
from src.coletaveis.coletaveis import Item

class GarrafaPitu(Item):
    def __init__(self, pos):
        super().__init__("Garrafa de Pitú", pos, 'pitu.png', 2, 60, 190, 10, 32)

    def aplicar_efeito(self, professor):
        super().aplicar_efeito(professor)
        professor.drunk = True
        professor.tempo_drunk = pygame.time.get_ticks() + 7000 # 7 segundos de tontura

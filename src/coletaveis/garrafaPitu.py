import pygame
from src.coletaveis.item import Item

class GarrafaPitu(Item):
    def __init__(self, pos, duracao_ms):
        super().__init__("Garrafa de Pitú", pos, 'pitu.png', 2, 60, 190, 10, 32)
        self.duracao_ms = duracao_ms
    
    def aplicar_efeito(self, professor):
        professor.drunk = True
        professor.tempo_drunk = pygame.time.get_ticks() + self.duracao_ms

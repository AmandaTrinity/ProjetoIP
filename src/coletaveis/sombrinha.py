import pygame
from src.utils.audio import som_sombrinha
from src.coletaveis.coletaveis import Item

class SombrinhaFrevo(Item):
    def __init__(self, pos):
        super().__init__("Sombrinha de Frevo", pos, 'sprite_sheetsombrinha.png', 3, 26, 26)
        
    def aplicar_efeito(self, professor):
        super().aplicar_efeito(professor)
        som_sombrinha.play()
        professor.velocidade = professor.velocidade_base * 2
        professor.tempo_boost = pygame.time.get_ticks() + 5000 # 5 segundos de boost

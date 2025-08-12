import pygame
from src.coletaveis.item import Item
from src.settings import *

class SombrinhaFrevo(Item):
    def __init__(self, pos):
        super().__init__("Sombrinha de Frevo", pos, 'sprite_sheetsombrinha.png', 3, 26, 26)
    
    def aplicar_efeito(self, professor):
        pygame.mixer.Channel(0).pause()
        professor.canal_efeitos.play(professor.som_sombrinha)
        professor.velocidade = VELOCIDADE_JOGADOR * 2
        professor.tempo_boost = pygame.time.get_ticks() + DURACAO_BOOST_MS

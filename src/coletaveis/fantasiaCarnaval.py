import pygame
from src.coletaveis.item import Item
from src.utils.constantes import *

class FantasiaCarnaval(Item):
    def __init__(self, pos):
        super().__init__("Máscara de Carnaval", pos, 'FantasiaVampiro 19x25.png', 1, 19, 25)
    
    def aplicar_efeito(self, professor):
        professor.tipo = 'vampiro '
        professor.invisivel = True
        professor.tempo_invisivel = pygame.time.get_ticks() + DURACAO_INVISIBILIDADE_MS
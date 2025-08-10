import pygame
from src.coletaveis.coletaveis import Item

class FantasiaCarnaval(Item):
    def __init__(self, pos):
        super().__init__("Máscara de Carnaval", pos, 'FantasiaVampiro 19x25.png', 1, 19, 25)

    def aplicar_efeito(self, professor):
        super().aplicar_efeito(professor)
        professor.tipo = 'vampiro ' #troca a fantasia
        professor.invisivel = True
        professor.tempo_invisivel = pygame.time.get_ticks() + 8000 # 8 segundos de invisibilidade
        professor.image.set_alpha(128) # Fica semitransparente

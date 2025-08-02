import pygame
import random

from config import *

# HERANÇA: classe mãe.
# para itens colecionáveis
class Coletavel:

    # algumas definições de fábrica
    def __init__(self):

        # atualmente o coletável é um quadrado menor e vermelho
        self.image = pygame.Surface((30, 30))
        self.rect = self.image.get_rect()

        # chamar respawn pra definir posicao inicial
        self.respawn()
    
    def respawn(self):

        # biblioteca random para poisicionar o coletável em um lugar aleatório na tela
        self.rect.x = random.randint(0, tela_largura - self.rect.width)
        self.rect.y = random.randint(0, tela_altura - self.rect.height)

# HERANÇA: classes filhas
class Moeda(Coletavel):

    def __init__(self):
        # super().__init__() chama o construtor da classe mãe
        # Moeda, COMO FILHA, terá tudo que a mãe tem direito
        super().__init__()
        self.image.fill(amarelo)

class Pocao(Coletavel):

    def __init__(self):

        super().__init__()
        self.image.fill(verde)
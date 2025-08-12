import pygame
import random
from src.utils.constantes import *

def encontrar_posicoes_acessiveis(layout, inicio_i, inicio_j):
    """Encontra todas as posições 'C' alcançáveis a partir de um ponto."""
    fila = [(inicio_i, inicio_j)]
    visitados = set([(inicio_i, inicio_j)])
    acessiveis = []
    while fila:
        i, j = fila.pop(0)
        if layout[i][j] == 'C':
            x = j * TAMANHO_BLOCO + TAMANHO_BLOCO // 2
            y = i * TAMANHO_BLOCO + TAMANHO_BLOCO // 2
            acessiveis.append((x, y))
        for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < len(layout) and 0 <= nj < len(layout[0]):
                if layout[ni][nj] != 'P' and (ni, nj) not in visitados:
                    visitados.add((ni, nj))
                    fila.append((ni, nj))
    return acessiveis

def criar_labirinto(lista_telhados):
    """Cria os sprites de parede e encontra posições de entrada/saída."""
    paredes = pygame.sprite.Group()
    pos_entrada_rect, pos_saida_rect, pos_entrada_centro = None, None, None
    inicio_i, inicio_j = -1, -1
    for i, linha in enumerate(LAYOUT_LABIRINTO):
        for j, celula in enumerate(linha):
            x, y = j * TAMANHO_BLOCO, i * TAMANHO_BLOCO
            if celula == 'P':
                paredes.add(Parede(x, y, lista_telhados))
            elif celula == 'E':
                pos_entrada_rect = pygame.Rect(x, y, TAMANHO_BLOCO, TAMANHO_BLOCO)
                pos_entrada_centro = (x + TAMANHO_BLOCO // 2, y + TAMANHO_BLOCO // 2)
                inicio_i, inicio_j = i, j
            elif celula == 'S':
                pos_saida_rect = pygame.Rect(x, y, TAMANHO_BLOCO, TAMANHO_BLOCO)
    
    posicoes_validas = []
    if inicio_i != -1:
        posicoes_validas = encontrar_posicoes_acessiveis(LAYOUT_LABIRINTO, inicio_i, inicio_j)
    
    return paredes, posicoes_validas, pos_entrada_centro, pos_entrada_rect, pos_saida_rect

class Parede(pygame.sprite.Sprite):
    def __init__(self, x, y, lista_telhados):
        super().__init__()
        self.image = random.choice(lista_telhados)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
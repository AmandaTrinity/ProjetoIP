import pygame
import random
from src.utils.constantes import TAMANHO_BLOCO, LAYOUT_LABIRINTO, IMAGENS_DIR

def encontrar_posicoes_acessiveis(layout, inicio_i, inicio_j):
    """Encontra todas as posições acessíveis a partir de um ponto inicial usando BFS."""
    fila = [(inicio_i, inicio_j)]
    visitados = set([(inicio_i, inicio_j)])
    acessiveis = []

    while fila:
        i, j = fila.pop(0)
        
        # Se for um corredor, adiciona às posições acessíveis para spawn de itens
        if layout[i][j] == 'C':
            x = j * TAMANHO_BLOCO + TAMANHO_BLOCO // 2
            y = i * TAMANHO_BLOCO + TAMANHO_BLOCO // 2
            acessiveis.append((x, y))

        # Verifica os vizinhos (cima, baixo, esquerda, direita)
        for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            ni, nj = i + di, j + dj

            # Checa se o vizinho está dentro dos limites do labirinto
            if 0 <= ni < len(layout) and 0 <= nj < len(layout[0]):
                # Checa se não é uma parede e se ainda não foi visitado
                if layout[ni][nj] != 'P' and (ni, nj) not in visitados:
                    visitados.add((ni, nj))
                    fila.append((ni, nj))
    
    return acessiveis

def criar_labirinto(lista_telhados):
    """Cria os sprites do labirinto e retorna as posições válidas."""
    paredes = pygame.sprite.Group()
    pos_entrada_rect = None
    pos_saida_rect = None
    pos_entrada_centro = None
    inicio_i, inicio_j = -1, -1 # Coordenadas da matriz para o início do BFS

    for i, linha in enumerate(LAYOUT_LABIRINTO):
        for j, celula in enumerate(linha):
            x, y = j * TAMANHO_BLOCO, i * TAMANHO_BLOCO
            if celula == 'P':
                paredes.add(Parede(x, y, lista_telhados))
            elif celula == 'E':
                pos_entrada_rect = pygame.Rect(x, y, TAMANHO_BLOCO, TAMANHO_BLOCO)
                pos_entrada_centro = (x + TAMANHO_BLOCO // 2, y + TAMANHO_BLOCO // 2)
                inicio_i, inicio_j = i, j # Guarda a posição inicial
            elif celula == 'S':
                pos_saida_rect = pygame.Rect(x, y, TAMANHO_BLOCO, TAMANHO_BLOCO)

    # Agora, encontra as posições realmente acessíveis
    if inicio_i != -1:
        posicoes_validas = encontrar_posicoes_acessiveis(LAYOUT_LABIRINTO, inicio_i, inicio_j)
    else:
        posicoes_validas = [] # Caso não encontre a entrada

    return paredes, posicoes_validas, pos_entrada_centro, pos_entrada_rect, pos_saida_rect

class Parede(pygame.sprite.Sprite):
    """Classe para as paredes do labirinto"""
    def __init__(self, x, y, lista_telhados):
        super().__init__()
        self.image = random.choice(lista_telhados)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image) #Para não empacar nas paredes, o contato será somente com pixel direto
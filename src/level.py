# src/level.py
import pygame
import random
from settings import *
from sprites import Parede, Professor, Aluno, SombrinhaFrevo, GarrafaPitu, FantasiaCarnaval

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

def setup_fase(fase, lista_telhados, sons):
    """Configura todos os elementos para uma nova fase."""
    if fase == 1:
        num_alunos = 2
        duracao_pitu = DURACAO_PITU_FASE1_MS
    elif fase == 2:
        num_alunos = 3
        duracao_pitu = DURACAO_PITU_FASE2_MS
    else: # Fase 3 e outras
        num_alunos = 4
        duracao_pitu = DURACAO_PITU_FASE3_MS

    paredes, pos_validas, pos_e_centro, pos_e_rect, pos_s_rect = criar_labirinto(lista_telhados)
    
    sons_efeitos = {'sombrinha': sons['sombrinha']}
    professor = Professor(*pos_e_centro, sons['andando'], sons_efeitos)
    
    # Restringe áreas para posicionamento de alunos
    indices_restritos = {(5, 11), (6, 11), (7, 11), (8, 11), (9, 11), (10, 11), (5, 13), (6, 13), (7, 13), (8, 13)}
    pos_validas_para_alunos = [
        pos for pos in pos_validas 
        if ((pos[1] - TAMANHO_BLOCO // 2) // TAMANHO_BLOCO, (pos[0] - TAMANHO_BLOCO // 2) // TAMANHO_BLOCO) not in indices_restritos
    ]
    
    # Posiciona Alunos
    num_alunos = min(num_alunos, len(pos_validas_para_alunos))
    pos_alunos = random.sample(pos_validas_para_alunos, num_alunos)
    alunos = pygame.sprite.Group()
    for pos in pos_alunos:
        alunos.add(Aluno(pos[0] - TAMANHO_BLOCO // 2, pos[1] - TAMANHO_BLOCO // 2))

    # Posiciona Itens
    pos_alunos_set = set(pos_alunos)
    pos_validas_para_itens = [pos for pos in pos_validas if pos not in pos_alunos_set]
    pos_itens = random.sample(pos_validas_para_itens, min(3, len(pos_validas_para_itens)))
    
    itens = pygame.sprite.Group()
    if len(pos_itens) > 0: itens.add(SombrinhaFrevo(pos_itens[0]))
    if len(pos_itens) > 1: itens.add(GarrafaPitu(pos_itens[1], duracao_pitu))
    if len(pos_itens) > 2: itens.add(FantasiaCarnaval(pos_itens[2]))

    todos_sprites = pygame.sprite.Group(professor)
    hud_vars = {'sombrinha_coletada': False, 'pitu_coletada': False, 'mascara_coletada': False, 'mensagens': [f"FASE {fase}!"]}
    
    return {
        'paredes': paredes,
        'professor': professor,
        'todos_sprites': todos_sprites,
        'itens': itens,
        'alunos': alunos,
        'hud_vars': hud_vars,
        'pos_entrada': pos_e_rect,
        'pos_saida': pos_s_rect
    }
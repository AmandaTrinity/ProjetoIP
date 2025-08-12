# src/level.py
import pygame
import random
from src.utils.constantes import *
from src.personagens.professor import Professor
from src.personagens.aluno import Aluno
from src.coletaveis.fantasiaCarnaval import FantasiaCarnaval
from src.coletaveis.garrafaPitu import GarrafaPitu
from src.coletaveis.sombrinha import SombrinhaFrevo
from src.labirinto.labirinto import criar_labirinto

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
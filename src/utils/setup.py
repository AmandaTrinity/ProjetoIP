import pygame
import random
from src.labirinto.labirinto import criar_labirinto
from src.utils.constantes import *
from src.coletaveis.sombrinha import SombrinhaFrevo
from src.coletaveis.garrafaPitu import GarrafaPitu
from src.coletaveis.fantasiaCarnaval import FantasiaCarnaval
from src.personagens.professor import Professor
from src.personagens.aluno import Aluno

def iniciar_jogo(lista_telhados):
    paredes,pos_validas,pos_e_centro,pos_e_rect,pos_s_rect = criar_labirinto(lista_telhados)
    professor = Professor(*pos_e_centro)

    if len(pos_validas) >= 3:
        pos_itens = random.sample(pos_validas, 3)
    else:
        print("AVISO: Não há posições válidas suficientes para todos os itens!")
        pos_itens = pos_validas # Coloca itens onde for possível
    
    itens = pygame.sprite.Group()
    if len(pos_itens) > 0: itens.add(SombrinhaFrevo(pos_itens[0]))
    if len(pos_itens) > 1: itens.add(GarrafaPitu(pos_itens[1]))
    if len(pos_itens) > 2: itens.add(FantasiaCarnaval(pos_itens[2]))
    
    todos_sprites = pygame.sprite.Group(professor)
    
    # Adiciona alunos
    alunos = pygame.sprite.Group()
    alunos.add(Aluno(5 * TAMANHO_BLOCO, 7 * TAMANHO_BLOCO))
    alunos.add(Aluno(13 * TAMANHO_BLOCO, 2 * TAMANHO_BLOCO))

    tempo_inicio = pygame.time.get_ticks()

    return paredes, pos_e_rect, pos_s_rect, professor, itens, todos_sprites, alunos, tempo_inicio
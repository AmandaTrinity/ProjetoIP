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

# Carrega as fontes usadas no jogo
def carregar_fontes():
    fonte_grande = pygame.font.Font(None, 74)
    fonte_media = pygame.font.Font(None, 50)
    fonte_pequena = pygame.font.Font(None, 36)
    return fonte_grande, fonte_media, fonte_pequena

def carregar_recursos():
    # Carrega a sprite sheet dos telhados e cria uma lista de imagens individuais
    spritesheet_telhados = pygame.image.load(os.path.join(SPRITES_DIR, 'telhadoscoloridos.png')).convert()
    lista_telhados = []
    for i in range(6): # O número de telhados de cores diferentes na sprite sheet
        imagem_telhado = spritesheet_telhados.subsurface((i * 40, 0), (40, 40))
        lista_telhados.append(imagem_telhado)

    # Carrega a imagem de fundo do jogo
    try:
        caminho_fundo = os.path.join(SPRITES_DIR, 'chãojogo.jpg')
        imagem_fundo=pygame.image.load(caminho_fundo).convert()
        imagem_fundo = pygame.transform.scale(imagem_fundo, (LARGURA_TELA, ALTURA_TELA))
        print("Imagem de fundo carreagado com sucesso!")
    except pygame.error as e:
        print(f"Erro ao carregar imagem: {e}")
        imagem_fundo = None # Se a imagem falhar, usaremos uma cor de fundo sólida
    return lista_telhados, imagem_fundo
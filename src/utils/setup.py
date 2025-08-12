import pygame
import os
import sys
from src.utils.constantes import *

def carregar_animacao(caminho_base, prefixo_arquivo, num_frames, novo_tamanho):
    """Carrega uma sequência de imagens e a retorna como uma lista de surfaces."""
    frames = []
    for i in range(num_frames):
        nome_arquivo = f"{prefixo_arquivo}{i}.png"
        caminho_completo = os.path.join(caminho_base, nome_arquivo)
        try:
            imagem = pygame.image.load(caminho_completo).convert_alpha()
            frames.append(pygame.transform.scale(imagem, novo_tamanho))
        except pygame.error as e:
            print(f"Erro ao carregar frame '{caminho_completo}': {e}")
            fallback_surface = pygame.Surface(novo_tamanho)
            fallback_surface.fill(VERMELHO)
            frames.append(fallback_surface)
    return frames

def carregar_recursos_globais():
    """Carrega todos os assets visuais e fontes globais do jogo."""
    try:
        ss_telhados = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'telhadoscoloridos.png')).convert()
        lista_telhados = [ss_telhados.subsurface((i * 40, 0), (40, 40)) for i in range(6)]
        fundo_img = pygame.transform.scale(pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'chãojogo.jpg')).convert(), (LARGURA_TELA, ALTURA_TELA))
        spritesheet_porta = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'porta_entrada_saida.png')).convert_alpha()
        lista_sprites_porta = [spritesheet_porta.subsurface((i * TAMANHO_BLOCO, 0), (TAMANHO_BLOCO, TAMANHO_BLOCO)) for i in range(4)]
        caminho_fonte = os.path.join(DIRETORIO_FONTES, 'PressStart2P-Regular.ttf')
        fontes = {
            'grande': pygame.font.Font(caminho_fonte, 36), 'media': pygame.font.Font(caminho_fonte, 26),
            'pequena': pygame.font.Font(caminho_fonte, 16), 'mini': pygame.font.Font(caminho_fonte, 12),
            'minuscula': pygame.font.Font(caminho_fonte, 8)
        }
        icones_hud = {
            'sombrinha': pygame.transform.scale(pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'sprite_sheetsombrinha.png')).convert_alpha().subsurface((0,0), (26,26)), (40, 40)),
            'pitu': pygame.transform.scale(pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'pitu.png')).convert_alpha().subsurface((0,0), (60,190)), (20, 50)),
            'mascara': pygame.transform.scale(pygame.image.load(os.path.join(DIRETORIO_IMAGENS, 'FantasiaVampiro 19x25.png')).convert_alpha().subsurface((0,0), (19,25)), (35, 45))
        }
        return {
            'lista_telhados': lista_telhados, 'fundo_img': fundo_img, 'lista_sprites_porta': lista_sprites_porta,
            'fontes': fontes, 'icones_hud': icones_hud
        }
    except pygame.error as e:
        print(f"Erro fatal ao carregar assets essenciais: {e}")
        pygame.quit()
        sys.exit()

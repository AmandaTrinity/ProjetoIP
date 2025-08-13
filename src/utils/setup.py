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

        fundo_menu_original = pygame.image.load(os.path.join(DIRETORIO_SPRITES, 'JORNADA_FIRST_OFICIAL.png')).convert()
        fundo_menu_img = pygame.transform.scale(fundo_menu_original, (LARGURA_TOTAL, ALTURA_TELA))

        # FAZENDO OS BOTOES

        TAMANHO_BOTAO = (182, 70) 

        img_original_normal = pygame.image.load(os.path.join(DIRETORIO_SPRITES, 'Começar_clicado.png')).convert_alpha()
        img_original_clicado = pygame.image.load(os.path.join(DIRETORIO_SPRITES, 'botão_começar.png')).convert_alpha()

        # Agora redimensiona as imagens para o novo tamanho
        botao_normal_img = pygame.transform.scale(img_original_normal, TAMANHO_BOTAO)
        botao_clicado_img = pygame.transform.scale(img_original_clicado, TAMANHO_BOTAO)

        # botao do menu

        img_menu_normal = pygame.image.load(os.path.join(DIRETORIO_SPRITES, 'Menu_clicado.png')).convert_alpha()
        img_menu_clicado = pygame.image.load(os.path.join(DIRETORIO_SPRITES, 'botão_menu.png')).convert_alpha() 

        botao_menu_normal_img = pygame.transform.scale(img_menu_normal, TAMANHO_BOTAO)
        botao_menu_clicado_img = pygame.transform.scale(img_menu_clicado, TAMANHO_BOTAO)

        # botao reiniciar 
        img_original_normal_reiniciar = pygame.image.load(os.path.join(DIRETORIO_SPRITES, 'reiniciar_clicado.png')).convert_alpha()
        img_original_clicado_reiniciar = pygame.image.load(os.path.join(DIRETORIO_SPRITES, 'reiniciar_botão.png')).convert_alpha()

        botao_reiniciar_normal_img = pygame.transform.scale(img_original_normal_reiniciar, TAMANHO_BOTAO)
        botao_reiniciar_clicado_img = pygame.transform.scale(img_original_clicado_reiniciar, TAMANHO_BOTAO)
        
        # telas de transição
        transicao12_img = pygame.transform.scale(pygame.image.load(os.path.join(DIRETORIO_SPRITES, 'FASE1FASE2.png')).convert(), (LARGURA_TOTAL, ALTURA_TELA))
        transicao23_img = pygame.transform.scale(pygame.image.load(os.path.join(DIRETORIO_SPRITES, 'FASE2FASE3.png')).convert(), (LARGURA_TOTAL, ALTURA_TELA))

        # BOTOES DE SOM
        TAMANHO_ICONE_SOM = (35, 35)

        icone_som_ligado_original = pygame.image.load(os.path.join(DIRETORIO_SPRITES, 'COM_VOLUME_OFICIAL.png')).convert_alpha()
        icone_som_mudo_original = pygame.image.load(os.path.join(DIRETORIO_SPRITES, 'SEM_VOLUME_OFICIAL.png')).convert_alpha()

        icone_som_ligado = pygame.transform.scale(icone_som_ligado_original, TAMANHO_ICONE_SOM)
        icone_som_mudo = pygame.transform.scale(icone_som_mudo_original, TAMANHO_ICONE_SOM)

        fundo_estandarte_original = pygame.image.load(os.path.join(DIRETORIO_SPRITES, 'estandarte-clean-removebg-preview.png')).convert_alpha()

        TAMANHO_ESTANDARTE = (640, 800) 
        fundo_estandarte_img = pygame.transform.scale(fundo_estandarte_original, TAMANHO_ESTANDARTE)

        derrota_tempo_img = pygame.transform.scale(pygame.image.load(os.path.join(DIRETORIO_SPRITES, 'STEFAN_PERDE_TEMPO.png')).convert(), (LARGURA_TOTAL, ALTURA_TELA))
        derrota_laursa_img = pygame.transform.scale(pygame.image.load(os.path.join(DIRETORIO_SPRITES, 'STEFAN_PERDE_LAURSA.png')).convert(), (LARGURA_TOTAL, ALTURA_TELA))

        vitoria_img = pygame.transform.scale(pygame.image.load(os.path.join(DIRETORIO_SPRITES, 'STEFAN_WIN.png')).convert(), (LARGURA_TOTAL, ALTURA_TELA))

        return {
            'lista_telhados': lista_telhados, 'fundo_img': fundo_img, 'lista_sprites_porta': lista_sprites_porta,
            'fontes': fontes, 'icones_hud': icones_hud,
            'fundo_tela_inicial': fundo_menu_img,
            'fundo_transicao_1_2': transicao12_img,
            'fundo_transicao_2_3': transicao23_img,
            'icones_som': {'ligado': icone_som_ligado, 'mudo': icone_som_mudo},
            'fundo_estandarte': fundo_estandarte_img,
            'fundo_derrota_tempo': derrota_tempo_img,
            'fundo_derrota_laursa': derrota_laursa_img,
            'fundo_vitoria': vitoria_img,
            'imagens_botao_inicial': {'normal': botao_normal_img, 'clicado': botao_clicado_img},
            'imagens_botao_menu': {'normal': botao_menu_normal_img, 'clicado': botao_menu_clicado_img},
            'imagens_botao_reiniciar': {'normal': botao_reiniciar_normal_img, 'clicado': botao_reiniciar_clicado_img}
        }
    
    except pygame.error as e:
        print(f"Erro fatal ao carregar assets essenciais: {e}")
        pygame.quit()
        sys.exit()
